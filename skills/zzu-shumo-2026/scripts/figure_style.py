import hashlib  # 为绘图输入生成可追溯的文件指纹。
import json  # 保存与图片配套的机器检查记录。
import logging  # 捕获数学文本通过日志发出的缺字信息。
import math  # 检查显式分辨率是否为有限正数。
from contextlib import contextmanager  # 确保临时日志监听在异常后也能解除。
import re  # 核验中文图题及合法编号。
import warnings  # 捕获缺字并明确报告字体替代。
from pathlib import Path  # 使用跨平台路径定位输入与输出。
import matplotlib.pyplot as plt  # 按用户习惯导入绘图接口。
try:  # 只在选择 SciencePlots 时要求该可选依赖。
    import scienceplots  # 注册推荐样式；已有图的导出不必依赖它。
except ImportError:
    scienceplots = None
from matplotlib import font_manager  # 检查真实可用字体而非假定字体存在。
from matplotlib.text import Text  # 获取实际绘制的标题、坐标轴和图例文字。
from PIL import Image  # 核验最终 PNG 的像素尺寸和分辨率元数据。

PALETTE = ('#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00', '#56B4E9')  # 采用色觉友好的离散配色并要求同时区分线型。
LINESTYLES = ('-', '--', '-.', ':')  # 在黑白打印时保留曲线辨识度。

@contextmanager  # 将日志监听限定在当前一次图片导出中。
def _font_logs():  # 补充 Python warnings 无法捕获的 mathtext 缺字诊断。
    messages = []  # 保存此次渲染的字体日志。
    handler = logging.Handler()  # 使用临时处理器而不改变全局日志级别。
    handler.emit = lambda record: messages.append(record.getMessage())  # 收集原始文本以便检查是否替换成占位字形。
    logger = logging.getLogger('matplotlib')  # 子模块字体日志会传递到此记录器。
    logger.addHandler(handler)  # 开始监听实际渲染。
    try:  # 无论保存是否成功都执行清理。
        yield messages  # 将记录容器交给导出函数。
    finally:  # 不让其他绘图任务受到本次检查影响。
        logger.removeHandler(handler)  # 移除临时监听器。

def _prepare_mixed_text(fig, chinese_font):  # 修正同一标签中中文和数学文本混排的默认字体限制。
    for item in fig.findobj(Text):  # 包括坐标标签、图例、图题和用户文字。
        value = item.get_text()  # 读取用户提供的原始标签。
        if re.search(r'[\u4e00-\u9fff]', value) and '$' in value and item.get_parse_math():  # 只处理包含中文的数学混排文本。
            chunks = re.split(r'(\$(?:\\.|[^$])*\$)', value)  # 保留已有数学区，不改其中量符号的斜体含义。
            for index in range(0, len(chunks), 2):  # 非数学区的普通字母和数字也必须采用新罗马。
                chunks[index] = re.sub(r'[A-Za-z0-9]+', lambda match: r'$\mathrm{' + match.group(0) + '}$', chunks[index])  # 明确转换普通拉丁字母及数字，避免被中文默认字体覆盖。
            item.set_text(''.join(chunks))  # 将语义不变且字体明确的标签用于实际绘制。
            item.set_fontfamily(chinese_font)  # 非数学区由宋体渲染，数学区仍遵从 custom 新罗马设置。

def _drawn_texts(fig):  # 只检查会实际绘制的文本，排除范围外自动刻度。
    excluded = set()  # 保存 Axis 不会绘制的刻度标签身份。
    for ax in fig.axes:  # 分别查询每个坐标轴的真实可见刻度。
        for axis in (ax.xaxis, ax.yaxis):  # 同时覆盖横轴和纵轴。
            lower, upper = sorted(axis.get_view_interval())  # 同时适用于正常和反向坐标轴。
            tolerance = max(abs(upper - lower), 1e-12) * 1e-10  # 仅容许边界浮点舍入误差。
            for tick in (*axis.get_major_ticks(), *axis.get_minor_ticks()):  # 缓存中的刻度不一定在最终轴范围内。
                if not lower - tolerance <= tick.get_loc() <= upper + tolerance:  # 使用实际刻度位置过滤不会显示的标签。
                    excluded.update((id(tick.label1), id(tick.label2)))  # 保留边界内文字的正常越界审计。
    return [item for item in fig.findobj(Text) if id(item) not in excluded and item.get_visible() and item.get_text().strip()]  # 保留真正需要检查的文字。

def _choose_font(names):  # 按优先顺序查找字体并禁止静默回退到默认字体。
    for name in names:  # 先尝试指定字体，再考虑公开说明的替代字体。
        try:  # 当前平台没有该字体时继续检查下一种。
            path = font_manager.findfont(font_manager.FontProperties(family=name), fallback_to_default=False)  # 检查实际字体文件。
            return name, Path(path).name  # 报告字体名和文件名，不输出作者电脑的绝对路径。
        except ValueError:  # 字体不可用时采用后续候选。
            continue  # 继续尝试已列出的字体。
    raise RuntimeError(f'找不到指定字体候选：{names}；请选择已安装且覆盖所需字形的字体。')  # 不以缺字图片冒充合格输出。

def configure_style(strict_fonts=False, *, style='science', chinese_fonts=None, latin_fonts=None, rc_overrides=None):
    """新建图的可覆盖默认样式；已有图只作布局调整时不调用此函数。"""
    styles = [style] if isinstance(style, str) else list(style or ())
    if any(name in ('science', 'no-latex') for name in styles) and scienceplots is None:
        raise RuntimeError('SciencePlots 未安装；可使用已有环境中的样式或 style=None。')
    if styles:
        plt.style.use(styles)
    latin_candidates = latin_fonts or (('Times New Roman',) if strict_fonts else ('Times New Roman', 'Liberation Serif', 'DejaVu Serif'))
    chinese_candidates = chinese_fonts or (('SimSun',) if strict_fonts else ('SimSun', 'Songti SC', 'Noto Serif CJK SC', 'Source Han Serif SC'))
    latin_candidates = (latin_candidates,) if isinstance(latin_candidates, str) else tuple(latin_candidates)
    chinese_candidates = (chinese_candidates,) if isinstance(chinese_candidates, str) else tuple(chinese_candidates)
    latin, latin_file = _choose_font(latin_candidates)
    chinese, chinese_file = _choose_font(chinese_candidates)
    fallback = latin != latin_candidates[0] or chinese != chinese_candidates[0]
    if fallback:  # 替代字体须清楚说明，不能宣称已经使用宋体和新罗马。
        warnings.warn(f'字体替代：中文使用 {chinese}，英文和数字使用 {latin}；请人工确认。', UserWarning, stacklevel=2)  # 显示实际渲染设置。
    plt.rcParams.update({'text.usetex': False, 'font.family': [latin, chinese], 'font.size': 10, 'axes.labelsize': 10, 'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 9, 'axes.linewidth': 0.7, 'lines.linewidth': 1.25, 'lines.markersize': 4, 'axes.prop_cycle': plt.cycler(color=PALETTE), 'axes.spines.top': False, 'axes.spines.right': False, 'xtick.top': False, 'ytick.right': False, 'xtick.direction': 'in', 'ytick.direction': 'in', 'axes.unicode_minus': True, 'legend.frameon': False, 'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.facecolor': 'white', 'savefig.dpi': 600, 'mathtext.fontset': 'custom', 'mathtext.rm': latin, 'mathtext.it': f'{latin}:italic', 'mathtext.bf': f'{latin}:bold', 'mathtext.bfit': f'{latin}:bold:italic', 'mathtext.cal': 'STIXGeneral:italic', 'mathtext.sf': latin, 'mathtext.tt': latin, 'mathtext.fallback': 'stix', 'pdf.fonttype': 42, 'ps.fonttype': 42})  # 关闭外部 TeX，普通文本按字形依次选字体，复杂数学符号允许 STIX 补字。
    if rc_overrides:  # 字号、线宽、配色等服从本次模板；字体候选通过上面的专用参数指定。
        if any(key.startswith('font.') and key != 'font.size' for key in rc_overrides) or any(key.startswith('mathtext.') for key in rc_overrides):
            raise ValueError('字体族请用 chinese_fonts/latin_fonts 设置；其他字体体系可由调用者自行配置并直接导出。')
        plt.rcParams.update(rc_overrides)
    return {'chinese': chinese, 'latin_digits': latin, 'chinese_file': chinese_file, 'latin_file': latin_file, 'fallback_used': fallback, 'math': f'{latin} + STIX fallback', 'external_tex': bool(plt.rcParams['text.usetex']), 'styles': styles}  # 后续质检须保留真实字体状态。

def new_figure(width_mm=160, height_mm=105, nrows=1, ncols=1, *, caption_space=0.11, **kwargs):
    """按毫米建图；Word 原生题注场景使用 caption_space=0，消除预留题注区。"""
    if width_mm <= 0 or height_mm <= 0:  # 物理尺寸必须为正数。
        raise ValueError('图像宽度和高度必须大于零。')  # 在绘制前阻止无效版面。
    if not 0 <= caption_space < 1:
        raise ValueError('题注预留比例须在 [0, 1) 内。')
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(width_mm / 25.4, height_mm / 25.4), layout='constrained', **kwargs)  # 毫米换算为英寸。
    fig.get_layout_engine().set(rect=(0, caption_space, 1, 1 - caption_space))
    return fig, axes  # 返回标准 Matplotlib 对象以保留完整可定制能力。

def add_figure_title(fig, number, title):  # 将图序和简明中文图题置于图下方。
    if not re.fullmatch(r'[1-9]\d*(?:[.-][1-9]\d*)?', str(number)) or not re.search(r'[\u4e00-\u9fff]', title):  # 编号必须明确且图题必须包含中文。
        raise ValueError('请提供正整数或章节式图序，以及明确的中文图题。')  # 不生成占位标题。
    if '\n' in title:  # 单行简明图题有助于稳定预留高度。
        raise ValueError('请使用单行简明中文图题；详细说明放在正文。')  # 解释性图注不放到图下。
    if getattr(fig, '_zzu_title', None) is not None:  # 重复调用时更新已有图题。
        fig._zzu_title.remove()  # 避免同一图中叠加两条题目。
    fig._zzu_title = fig.text(0.5, 0.027, f'图 {number} {title}', ha='center', va='bottom', fontsize=10)  # 仅保留图序和图题，无解释性图注。
    return fig._zzu_title  # 返回文字对象供特殊布局显式调整。

def three_line_table(headers, rows, number, title, width_mm=160, height_mm=72):  # 绘制三线表 PNG 预览；可编辑论文表格另用 word_tables.py。
    if not headers or not rows or any(len(row) != len(headers) for row in rows):  # 保证行列关系明确。
        raise ValueError('三线表需要非空且列数一致的表头和数据。')  # 不隐式丢弃或补齐单元格。
    if not re.fullmatch(r'[1-9]\d*(?:[.-][1-9]\d*)?', str(number)) or not re.search(r'[\u4e00-\u9fff]', title):  # 表题同样需要合法序号和中文。
        raise ValueError('请提供有效表序和中文表题。')  # 阻止遗漏表格标识。
    fig, ax = plt.subplots(figsize=(width_mm / 25.4, height_mm / 25.4))  # 建立固定输出尺寸的表格画布。
    ax.set_position((0.06, 0.07, 0.88, 0.76))  # 表题置上方并为三条横线预留空间。
    ax.set_axis_off()  # 移除坐标轴和所有无关框线。
    count = len(headers)  # 确定均匀列宽的列数。
    step = 0.86 / (len(rows) + 1)  # 由行数分配行高。
    for col, header in enumerate(headers):  # 将表头放在第一行中央。
        ax.text((col + 0.5) / count, 0.93 - step / 2, header, ha='center', va='center', transform=ax.transAxes)  # 可用数学文本区分斜体物理量与正体单位。
    for row_index, row in enumerate(rows):  # 数据按原始行序呈现。
        for col, value in enumerate(row):  # 逐格保留调用者明确提供的文本和精度。
            ax.text((col + 0.5) / count, 0.93 - step * (row_index + 1.5), str(value), ha='center', va='center', transform=ax.transAxes)  # 数字由新罗马字体渲染。
    for y, width in ((0.93, 1.0), (0.93 - step, 0.6), (0.07, 1.0)):  # 仅保留顶线、表头分隔线和底线。
        ax.plot((0, 1), (y, y), transform=ax.transAxes, color='black', linewidth=width, clip_on=False)  # 不添加竖线、底纹或其他内部横线。
    fig._zzu_title = fig.text(0.5, 0.91, f'表 {number} {title}', ha='center', va='center', fontsize=10)  # 表序和中文表题位于表格上方。
    return fig, ax  # 返回对象以便导出和必要的人工布局修正。

def save_png(fig, filename, font_report=None, source_files=(), alignment_groups=(), *, dpi=600, require_title=True, prepare_mixed_text=True, write_report=True):
    """默认导出 600 dpi；支持模板分辨率及无内嵌题注，已有图可不提供字体报告。"""
    if isinstance(dpi, bool) or not isinstance(dpi, (int, float)) or not math.isfinite(dpi) or dpi <= 0:
        raise ValueError('dpi 必须为有限正数。')
    requested_dpi = dpi
    path = Path(filename)  # 将用户指定路径转换为跨平台对象。
    if path.suffix.lower() != '.png':  # 本技能的默认交付格式固定为 PNG。
        raise ValueError('输出文件扩展名必须是 .png。')  # 不静默导出其他格式。
    if require_title and getattr(fig, '_zzu_title', None) is None:  # 文档中另设题注时由调用者明确关闭此检查。
        raise ValueError('请先添加中文图题，或使用三线表绘制函数。')  # 防止标题缺失的成品交付。
    sources = []  # 记录实际输入文件的版本而非编造来源。
    for item in source_files:  # 逐个检查调用者声明的真实输入。
        source = Path(item)  # 输入可以来自当前项目任意合法位置。
        sources.append({'file': source.name, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})  # 读取失败直接终止，禁止伪造溯源记录。
    path.parent.mkdir(parents=True, exist_ok=True)  # 只创建用户指定的输出目录。
    errors = []  # 汇总机器检查失败原因。
    if font_report and prepare_mixed_text and not font_report.get('external_tex', False):
        _prepare_mixed_text(fig, font_report['chinese'])  # 可关闭，避免改动已有图的文字或字体。
    with warnings.catch_warnings(record=True) as captured, _font_logs() as font_logs, plt.rc_context({'savefig.bbox': None}):  # 禁止 SciencePlots 紧裁切并监听两种缺字通道。
        warnings.simplefilter('always')  # 不因重复警告缓存遗漏缺字。
        fig.canvas.draw()  # 布局与文字包围盒必须以实际绘制结果为准。
        renderer = fig.canvas.get_renderer()  # 获取当前画布渲染器。
        outer = fig.bbox  # 最终画布边界用于检测文字裁切风险。
        visible = _drawn_texts(fig)  # 排除未显示的空白文字和范围外刻度。
        for item in visible:  # 检查标题、坐标刻度、标签和图例文字是否超出画布。
            bounds = item.get_window_extent(renderer)  # 读取文字实际尺寸。
            if bounds.x0 < outer.x0 - 1 or bounds.y0 < outer.y0 - 1 or bounds.x1 > outer.x1 + 1 or bounds.y1 > outer.y1 + 1:  # 允许一个显示像素的舍入误差。
                errors.append(f'文字超出画布：{item.get_text()}')  # 记录需调整布局的具体文字。
        for group in alignment_groups:  # 仅检查调用者明确声明可比的同一排子图。
            positions = [axis.get_position() for axis in group]  # 色条和嵌套坐标轴不要纳入该组。
            if len(positions) > 1:  # 单图不存在组内对齐问题。
                spread = max(max(getattr(p, attr) for p in positions) - min(getattr(p, attr) for p in positions) for attr in ('y0', 'y1'))  # 检查同一行子图上下边缘一致。
                if spread * fig.get_figheight() * 72 > 1.5:  # 一点五磅为此助手的内部布局容差而非比赛强制标准。
                    errors.append('同排子图上下边缘差异超过 1.5 pt。')  # 对指定可比面板报告对齐失败。
        fig.savefig(path, dpi=requested_dpi, format='png', facecolor=fig.get_facecolor(), transparent=False, bbox_inches=None)  # 不使用紧裁切，保持指定物理尺寸和图背景。
    missing = sorted({str(item.message) for item in captured if 'glyph' in str(item.message).lower() and 'missing' in str(item.message).lower()})  # 聚合缺字警告。
    missing.extend(message for message in font_logs if 'does not have a glyph' in message.lower() or 'dummy symbol' in message.lower())  # 数学文本占位符同样必须阻止交付。
    errors.extend(missing)  # 缺字使机器检查失败。
    with Image.open(path) as picture:  # 独立读取真实成品而不只检查保存参数。
        pixels, actual_dpi = picture.size, picture.info.get('dpi', (0, 0))  # 提取像素和 PNG 分辨率元数据。
    expected = tuple(round(value * requested_dpi) for value in fig.get_size_inches())
    if any(abs(a - b) > 1 for a, b in zip(pixels, expected)) or any(abs(value - requested_dpi) > 0.02 for value in actual_dpi):
        errors.append(f'PNG 像素尺寸或分辨率元数据不符合 {requested_dpi:g} dpi 设定。')
    report = {'file': path.name, 'machine_status': 'FAIL' if errors else 'PASS', 'pixels': pixels, 'dpi': actual_dpi, 'requested_dpi': requested_dpi, 'fonts': font_report, 'sources': sources, 'errors': errors, 'render_warnings': sorted({str(item.message) for item in captured}), 'checked': ['PNG dimensions and DPI', 'missing glyph warnings', 'text inside canvas', 'explicit same-row alignment groups'], 'visual_review': 'required: inspect text overlaps, data visibility, formulas, titles and line distinction at final size'}  # fonts 为 None 时表示调用者保留自己的字体配置。
    if write_report:  # 小修改可直接使用返回报告，不必为每次导出新增文件。
        path.with_suffix('.qa.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if errors:  # 失败图片保留便于诊断，但函数以异常阻止宣告交付成功。
        raise RuntimeError('图片检查失败：' + '；'.join(errors))  # 返回清楚的调整方向。
    return report  # 正常调用可继续执行人工视觉核查。
