# 方法目录与SPSSPRO入口

按当前任务查相应方法，不整体加载原始论文。这里的“完全对应”只指基础方法和任务类别；“部分对应”只覆盖组件或基础版本；“未覆盖”指本次没有找到可确认的专项帮助，不表示软件一定不支持。

前25项的频次来自2019—2021年114篇已读摘要的保守记录下界，不能推广到全部年份。新增跨年方法只作证据示例，不套用114分母。全部方法与出处见[完整方法报告](<evidence/method_catalog.md>)，正文段落级核验另见[方法正文证据](<evidence/方法正文证据.json>)。

数据划分、训练内拟合、独立单位和最终评估边界先按 data-preparation.md 与 model-validation.md 确定。G1/G2/G3分别指训练内拟合、按依赖结构划分、保留最终评估。

## M01 缺失值填补与时间插值

SPSSPRO：部分对应；[缺失值处理](https://www.spsspro.com/help/Missing-value/)。

输入与前提：含时间/组别索引的原始变量、缺失位置和连续缺失长度。 区分历史补全与未来预测；长段缺失和结构性缺失须单独判断。

核验：在已知区段人工遮蔽后比较重建误差；报告处理前后数量、时序连续性。 易误用：不能用未来观测插补训练时不可知的输入；均值填充不能保留原经验分布与不确定性。

本地依据：D19102470244.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。帮助覆盖统计填充及若干插值，不能据相同次数认定论文的局部拉格朗日实现完全相同。

方法边界来源：[scikit-learn：常见错误与数据泄漏](https://scikit-learn.org/stable/common_pitfalls.html)、[SciPy：拉格朗日插值的数值限制](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.lagrange.html)。

## M02 异常值判定：物理范围、IQR与3σ

SPSSPRO：部分对应；[异常值处理](https://www.spsspro.com/help/outlier/)。

输入与前提：原始测量值、单位、有效范围、测量状态及异常原因记录。 IQR标记是检查线索；3σ规则需结合分布与测量机制，极端真实事件不能自动删除。

核验：记录各规则命中数量及交集；核查保留/剔除样本；比较敏感性。 易误用：2021B样本原文IQR下界有误印，详见旧10条深证据报告；不把获奖等同公式正确。

本地依据：E20112870005.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。帮助可用于异常值处理；论文常联合物理规则和3σ，不能整体等同IQR自动剔除。

方法边界来源：[NIST：箱线图与IQR围栏](https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm)。

## M03 Z-score与尺度变换

SPSSPRO：完全对应；[数据标准化](https://www.spsspro.com/help/Data-standardization/)。

输入与前提：数值列、单位、训练样本范围与保存的中心/尺度参数。 先明确定量、类别与周期变量；零方差列单独处理。

核验：检查训练变换统计量与新样本复用过程；按通用G1执行。 易误用：标准化不等于正态化；不能把名义类别编号标准化成有意义的距离。

本地依据：B21100790043.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应基础Z-score处理，不代表自动确定指标正负向或完成模型训练分割。

方法边界来源：[scikit-learn：StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)。

## M04 Pearson线性相关

SPSSPRO：完全对应；[相关性分析](https://www.spsspro.com/help/correlation/)。

输入与前提：成对对齐的数值变量、样本独立单位、时间或组别标识。 非恒定变量；检查散点形态和极端点，检验所需抽样假设另行说明。

核验：报告r、样本数、区间或检验方法；多重比较和序列依赖单独处理。 易误用：相关不等于因果，低线性相关不等于独立；正态性不是计算r的必需条件。

本地依据：B21102510017.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。帮助含Pearson系数与显著性；需区分系数计算与参数检验假设。

方法边界来源：[SciPy：Pearson相关系数及推断](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html)。

## M05 Spearman秩相关

SPSSPRO：完全对应；[相关性分析](https://www.spsspro.com/help/correlation/)。

输入与前提：可排序数值或有序变量、成对观测、并列值处理规则。 变量顺序有实际含义；注明缺失处理、并列秩和独立观测假设。

核验：查看秩散点、系数和有效样本数；小样本可核对适当置换检验。 易误用：不能把故障类型等无序标签编码后直接解释秩相关；相关弱不证明独立。

本地依据：B20103380015.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应有意义秩次变量的单调关系分析。

方法边界来源：[SciPy：Spearman相关系数及推断](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html)。

## M06 PCA与核PCA降维

SPSSPRO：部分对应；[主成分分析PCA](https://www.spsspro.com/help/pca/)、[数据降维](https://www.spsspro.com/help/Dimension-reduction/)。

输入与前提：样本×特征矩阵、尺度定义、保留维数或方差目标。 明确PCA分析对象是样本还是变量；训练空间拟合后复用于新数据。

核验：报告解释方差、载荷/得分及重建或下游验证；检查保留维数敏感性。 易误用：主成分得分不是挑选的原变量；高解释方差不保证保留预测目标信息。

本地依据：D19105320030.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。基础线性PCA对应；核化、EOF、因子分析及特定通道选择规则不能自动视为同一实现。

方法边界来源：[scikit-learn：PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)。

## M07 K-means及初始化变体

SPSSPRO：完全对应；[聚类分析K-Means](https://www.spsspro.com/help/k-means/)。

输入与前提：可定义欧氏距离的特征矩阵、K候选范围、随机初始化设置。 考虑尺度及簇形状；不直接把名义类别整数编号当距离。

核验：比较多次初始化、轮廓系数与业务解释；报告K敏感性。 易误用：均值中心未必是实际样本；用同一数据造簇后做差异检验不能独立证明分类有效。

本地依据：D19102860085.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应K-means基本聚类；论文自定义的改进步骤或后续选片仍须独立复现。

方法边界来源：[scikit-learn：聚类方法与适用范围](https://scikit-learn.org/stable/modules/clustering.html)。

## M08 凝聚层次聚类

SPSSPRO：完全对应；[分层聚类](https://www.spsspro.com/help/hierarchical-cluster/)。

输入与前提：距离矩阵或数值特征、连接方法、聚类对象方向。 明确按样本还是按变量聚类；距离和连接方式必须与数据意义一致。

核验：展示树状图和截断规则；比较距离/连接方法敏感性。 易误用：不能省略距离定义；树状图有层次不表示自然真实类别已被证实。

本地依据：B20103380015.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应凝聚层次聚类；帮助不等同BIRCH或所有分裂式算法。

方法边界来源：[scikit-learn：聚类方法与适用范围](https://scikit-learn.org/stable/modules/clustering.html)。

## M09 EM高斯混合模型GMM

SPSSPRO：未覆盖；本次未核得专项帮助页。

输入与前提：连续特征矩阵、分量数、协方差结构及初始化配置。 检查协方差退化和收敛；变量尺度与分量数量需有依据。

核验：比较BIC/AIC、收敛日志、重启稳定性与分量解释。 易误用：EM收敛不保证全局最优；t-SNE二维分离不是GMM质量的充分证据。

本地依据：B20100040057.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。在已核验SPSSPRO来源中未找到能确认的GMM专项页；不以K-means或分层聚类替代。

方法边界来源：[scikit-learn：GaussianMixture](https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html)、[scikit-learn：高斯混合与EM算法](https://scikit-learn.org/stable/modules/mixture.html)。

## M10 特征筛选与融合：RFE、树重要性、相关/互信息

SPSSPRO：部分对应；[特征筛选](https://www.spsspro.com/help/Feature-filtering/)。

输入与前提：明确目标y、候选特征X、样本分组、选择预算与筛选参数。 按G1在训练折内筛选；区分有监督重要性、无监督过滤和后验解释。

核验：报告入选稳定性、全特征/简单筛选基线的同划分比较。 易误用：相关弱不是独立；重要性不是因果效应；先用全数据选特征再交叉验证会泄漏。

本地依据：B20102980116.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。帮助覆盖若干过滤、树重要性和RFE；论文的多阶段投票、mRMR-IFS或SHAP解释不能一键等同。

方法边界来源：[scikit-learn：特征选择](https://scikit-learn.org/stable/modules/feature_selection.html)、[scikit-learn：常见错误与数据泄漏](https://scikit-learn.org/stable/common_pitfalls.html)。

## M11 线性回归与普通最小二乘

SPSSPRO：完全对应；[线性回归最小二乘法](https://www.spsspro.com/help/linear-regression/)。

输入与前提：数值响应y、设计矩阵X、类别编码和观测单位。 明确是否含截距；估计、推断和预测各自假设分开说明。

核验：检查残差、共线性与样本外误差；参数解释附尺度与条件。 易误用：F检验显著不证明模型正确；R²不能单独证明泛化或因果。

本地依据：E19102470046.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应定量因变量OLS；非线性参数回归和几何定位最小二乘不自动包含。

方法边界来源：[SPSSPRO：线性回归最小二乘法](https://www.spsspro.com/help/linear-regression/)。

## M12 随机森林回归

SPSSPRO：完全对应；[随机森林回归](https://www.spsspro.com/help/random-forest-regressor/)。

输入与前提：特征X、定量y、独立验证集、树与采样参数。 响应定义和训练分布明确；不能用训练拟合代替预测评估。

核验：按G2/G3做同划分基线比较，报告MAE/RMSE及各子群误差。 易误用：树集成通常不擅长超出训练响应范围的外推；变量重要性不等于物理贡献。

本地依据：E19102470046.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应定量目标随机森林；融合/特征筛选流水线另行说明。

方法边界来源：[scikit-learn：RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)。

## M13 随机森林分类

SPSSPRO：完全对应；[随机森林分类](https://www.spsspro.com/help/random-forest-classifier/)。

输入与前提：X、语义明确的类别y、各类样本数和分组标识。 训练/测试标签意义一致；记录类别不平衡与阈值。

核验：混淆矩阵、各类召回/精确率、适当AUC和校准；按G2/G3比较。 易误用：总体准确率可能掩盖少数类失效；概率最大类不等同决策成本最优。

本地依据：D21101080006.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应分类目标森林；论文的类别重新定义不是软件帮助能替代的判断。

方法边界来源：[scikit-learn：交叉验证、分组与时序划分](https://scikit-learn.org/stable/modules/cross_validation.html)。

## M14 支持向量回归SVR

SPSSPRO：完全对应；[支持向量机SVR回归](https://www.spsspro.com/help/svm-regressor/)。

输入与前提：数值特征X、连续y、核函数、C、epsilon及核参数候选。 尺度处理按G1复用；SVR损失与预测单位明确。

核验：在训练内部调参，外部评价MAE/RMSE；检查支持向量比例和残差。 易误用：不能将SVM分类帮助当SVR；默认核参数没有跨题通用性。

本地依据：B20102980116.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应SVR定量预测；论文的特征选择和支持向量分类须分开。

方法边界来源：[scikit-learn：支持向量机](https://scikit-learn.org/stable/modules/svm.html)。

## M15 支持向量分类SVM

SPSSPRO：完全对应；[SVM分类](https://www.spsspro.com/help/svm-classifier/)。

输入与前提：数值X、离散y、受试者/轮次分组以及核与惩罚参数。 尺度与样本不平衡需处理；按G2选择验证单位。

核验：报告混淆矩阵、每类指标；调C/gamma并核对分组外表现。 易误用：SVC决策分数并非概率；有概率输出时也需校准验证。

本地依据：C20106980009.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。对应监督分类SVC；不包括S3VM等半监督扩展。

方法边界来源：[scikit-learn：支持向量机](https://scikit-learn.org/stable/modules/svm.html)。

## M16 梯度提升树家族：XGBoost、LightGBM、GBDT/HGBT

SPSSPRO：部分对应；[XGBoost回归](https://www.spsspro.com/help/xgboost-regressor/)。

输入与前提：X、y、损失定义、验证划分、树深/学习率/迭代配置。 区分回归和分类任务，保留调参验证与最终评估边界。

核验：同划分对比简单模型，报告学习曲线和样本外误差。 易误用：增加模型数量不是充分创新；多算法比较后仍需保留最终未参与选择的评估数据。

本地依据：B21100130067.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。该页能直接对应XGBoost回归；不能证明LightGBM、分类器和Stacking元学习器的同等实现。

方法边界来源：[scikit-learn：常见错误与数据泄漏](https://scikit-learn.org/stable/common_pitfalls.html)。

## M17 BP前馈网络与MLP回归

SPSSPRO：完全对应；[BP神经网络回归](https://www.spsspro.com/help/bp-regressor/)。

输入与前提：X、连续y、特征尺度、网络宽深、激活、损失与训练配置。 区分神经元机理模型与机器学习网络；初始化和参数量须记录。

核验：检查收敛曲线、重复种子及样本外误差；比较简单基线。 易误用：一次低训练损失不是高精度证明；网络名称不能代替结构和训练流程。

本地依据：B20102470089.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。基础前馈回归对应。网页检索返回官方正文，但本轮两次直接open返回内部错误；未验证在线运行。

方法边界来源：[scikit-learn：多层感知机](https://scikit-learn.org/stable/modules/neural_networks_supervised.html)。

## M18 CNN、LSTM、图网络与深度模型融合

SPSSPRO：未覆盖；本次未核得专项帮助页。

输入与前提：序列/图像/图结构张量、采样时钟、窗口定义、标签与对象分组。 输入轴、窗口重叠、空间邻接与预测时可得信息都需明确。

核验：按G2分组/时间外推验证；与不含时空模块的基线做消融，重复种子。 易误用：随机拆重叠窗口会造成近重复泄漏；模型拼接本身不证明有效。

本地依据：E20112870005.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。本轮未核得SPSSPRO对论文ResNet-LSTM、GRU-GCN或GAN组合的专项帮助；基础BP页不能充当等同链接。

方法边界来源：[scikit-learn：交叉验证、分组与时序划分](https://scikit-learn.org/stable/modules/cross_validation.html)。

## M19 ARIMA与季节性ARIMA

SPSSPRO：部分对应；[ARIMA](https://www.spsspro.com/help/ARIMA/)、[季节性ARIMA](https://www.spsspro.com/help/sarima/)。

输入与前提：等间隔序列、频率、时间范围、缺失处理和预测期。 差分、季节周期与外生信息设定须有数据依据。

核验：滚动起点评估、残差自相关、预测区间和不同预测步长误差。 易误用：随机打乱时间会高估效果；单次长远预测不等于已验证趋势。

本地依据：E19102470046.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。基础时序模型对应；与LSTM、Prophet等融合及长期外生变量预测不等同。

方法边界来源：[statsmodels：时序预测与滚动评估](https://www.statsmodels.org/stable/examples/notebooks/generated/statespace_forecasting.html)。

## M20 赋权与综合评价：熵权、AHP

SPSSPRO：部分对应；[熵值法](https://www.spsspro.com/help/entropy-method/)、[AHP简化版](https://www.spsspro.com/help/ahp/)。

输入与前提：指标矩阵和方向，或成对重要性判断矩阵及判断来源。 熵权依赖样本离散度；AHP需有可信判断来源，不可编造专家评分。

核验：检查权重和、方向及AHP一致性；对权重扰动做排序/决策敏感性分析。 易误用：AHP判断矩阵应为正互反矩阵，不能照搬帮助页‘对称矩阵’措辞；熵权大小不等于因果重要性。

本地依据：F21102540382.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。基础赋权对应；熵权和AHP来源不同，组合优化目标与完整模糊评价另须说明。

方法边界来源：[SPSSPRO：AHP简化版](https://www.spsspro.com/help/ahp/)、[SPSSPRO：熵值法](https://www.spsspro.com/help/entropy-method/)。

## M21 数学规划：线性、整数与非线性约束优化

SPSSPRO：部分对应；[规划求解](https://www.spsspro.com/help/programming-solution/)。

输入与前提：决策变量、单位、目标优先级、所有约束、变量类型及界限。 模型必须完整；线性化与放松后的可行性和等价性需说明。

核验：重算目标和逐约束残差；记录求解状态、界、gap和耗时；小例与精确解对照。 易误用：求解器返回值不自动是全局最优；不能把可行近似解写成已证明最优。

本地依据：F21102870035.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。帮助覆盖目标/约束/变量输入及若干求解器；不证明任意大规模整数排班、字典序目标和网络模型可直接同等求解。

方法边界来源：[SciPy：混合整数线性规划求解状态](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html)。

## M22 启发式与元启发式搜索

SPSSPRO：未覆盖；本次未核得专项帮助页。

输入与前提：目标函数、约束处理、编码、邻域/交叉变异、预算和随机种子。 需有可行解判定；比较算法应统一函数评估预算和停止规则。

核验：多次运行汇报可行率、目标分布与耗时；与简单策略/精确小例对照。 易误用：最优一次运行不能代表稳定优越；有限搜索通常不能证明全局最优。

本地依据：F20100070005.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。已核验规划帮助未覆盖论文使用的GA/PSO/DE/禁忌等完整自定义算法；不贴邻近概念充当专项页。

方法边界来源：[SciPy：差分进化](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.differential_evolution.html)。

## M23 蒙特卡洛仿真与随机试验

SPSSPRO：未覆盖；本次未核得专项帮助页。

输入与前提：明确随机变量分布、依赖关系、样本数、种子与输出统计量。 分布与抽样范围需要来源；模拟重复与真实独立重复需区分。

核验：报告估计量随样本量的稳定性、重复种子差异及适当模拟误差区间。 易误用：增加模拟次数不能消除模型设定偏差；模拟成功不证明现实必然成立。

本地依据：B19910160009.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。此前及本轮已核验帮助中未找到蒙特卡洛专项页；规划求解与随机搜索不是等同方法。

## M24 常微分方程与机理网络数值仿真

SPSSPRO：未覆盖；本次未核得专项帮助页。

输入与前提：方程、参数单位、初值、边界/输入、连接拓扑、时间步和误差容限。 方程适用范围与可识别参数分开说明；判断刚性及求解器适合性。

核验：步长/容限收敛、独立求解器交叉核对、极限情形和参数敏感性。 易误用：数值收敛不等于模型真实；数学仿真不能直接升级为临床疗效结论。

本地依据：C21102920019.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。未核得能对应HH回路、Euler/RK4及研究专用动力学的SPSSPRO专项页。

方法边界来源：[SciPy：常微分方程初值问题求解器](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)。

## M25 矩阵分解、迭代求逆与低秩压缩

SPSSPRO：未覆盖；本次未核得专项帮助页。

输入与前提：矩阵尺寸/类型、结构假设、目标秩、误差范数、精度阈值和实现基线。 检查共轭转置、秩及条件数；迭代初值与收敛条件须明确。

核验：核对分解残差和正交性；同时实测端到端耗时、峰值存储与重建误差。 易误用：仅引用渐近复杂度不能证明实测加速；压缩率改善必须与误差约束同时报告。

本地依据：A21102860059.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。PCA数据降维页不等于随机SVD、结构求逆和矩阵组压缩专项算法，未确认同等帮助。

方法边界来源：[NumPy：奇异值分解](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html)。

## M26 信号特征变换：FFT与小波分解

SPSSPRO：部分对应；[数据变换](https://www.spsspro.com/help/transform/)。

输入与前提：有序信号及采样间隔/空间间距、通道和单位；FFT的长度、归一化和窗口；小波基、分解层数与边界延拓方式。 按时间或空间含义确定变换轴，检查采样间距与缺失；判断去趋势、加窗、边界处理对所需特征的影响。

核验：用已知频率的合成信号核对频轴与幅值；比较窗函数及层数的敏感性，检查重构误差；若用于预测，按G1/G2在训练范围内确定预处理方案。 易误用：FFT点数增加或零填充不等于新增独立信息；幅度谱不自动等于功率谱密度。论文的四层小波不能直接套用帮助页的一级设置；边界伪影不能解释为真实局部结构。

本地依据：C90047002.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。官方页覆盖傅里叶、连续/离散小波变换；帮助中的基础变换与一级分解描述不能等同论文的FFT特征提取或四层小波残差分解流程。

方法边界来源：[SciPy：采样信号的谱分析、窗口与频谱归一化](https://docs.scipy.org/doc/scipy/tutorial/signal.html)、[PyWavelets：离散小波分解与有效层数](https://pywavelets.readthedocs.io/en/latest/ref/dwt-discrete-wavelet-transform.html)。

## M27 TOPSIS多指标评价

SPSSPRO：完全对应；[优劣解距离法TOPSIS](https://www.spsspro.com/help/TOPSIS/)。

输入与前提：评价对象×指标矩阵、每个指标的方向与单位、权重来源、比较对象范围和缺失处理记录。 先明确效益型、成本型及需要自行变换的中间型/区间型指标；固定正向化、归一化、距离和权重计算定义，处理恒定指标。

核验：逐步复核正负理想解、距离、接近度及排序；对权重、归一化方案与评价对象集合变化作敏感性分析，并核对领域含义。 易误用：接近度不是患病概率或绝对质量值；熵权反映样本离散度，不证明因果重要性。软件内部平移和归一化不保证与论文实现一致，不能仅凭排序输出声称方案已验证。

本地依据：E22106110005.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第3页，摘要声明。基础TOPSIS与熵权设置有直接帮助页；这里只确认评价组件，对论文后续K-means等级划分和优化求解不作等同认定。

方法边界来源：[SPSSPRO：TOPSIS的正向化、归一化与距离计算](https://www.spsspro.com/help/TOPSIS/)。

## M28 SHAP模型解释与特征贡献

SPSSPRO：未覆盖；本次未核得专项帮助页。

输入与前提：已经拟合且验证过的模型、训练预处理流程、待解释样本、背景数据、输出类别/输出尺度、解释器及版本。 解释器须适合模型类型；说明背景分布和相关特征的处理方式，区分原始输出、对数几率及概率空间；本地摘要未证明具体解释器选择正确。

核验：在同一模型输出尺度核对基线加贡献的加和关系；比较背景样本与相关特征设定的敏感性，报告全局汇总与具体样本解释各自范围。 易误用：SHAP解释的是模型预测，不能直接写成因果效应、作用机制或临床疗效；有正贡献不表示增加该特征在现实中必然改善结果。TreeExplainer也不自动适用于论文的深度网络。

本地依据：D21104860088.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。本轮按SHAP及Shapley检索SPSSPRO帮助，未找到可确认的专项页；已有特征筛选或树重要性页不能等同SHAP。社区旧答复不作为当前产品功能结论。

方法边界来源：[SHAP：TreeExplainer的背景、输出空间和加和关系](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html)、[SHAP：预测解释与因果解释的区别](https://shap.readthedocs.io/en/latest/example_notebooks/overviews/Be%20careful%20when%20interpreting%20predictive%20models%20in%20search%20of%20causal%20insights.html)。

## M29 卡方独立性检验与列联表关联分析

SPSSPRO：完全对应；[Pearson卡方检验](https://www.spsspro.com/help/pearson_chi/)。

输入与前提：独立个体的类别记录或真实计数列联表、类别定义、缺失情况；批量位点分析还需样本匹配、质控及检验数量。 每个计数须来自正确的独立单位；检查期望频数和稀疏单元，必要时使用与设计相符的精确或重抽样方法；配对数据不能当独立样本。

核验：保存观测/期望频数、自由度、检验变体、统计量和p值；结合效应量；批量检验报告校正策略及校正前后结果。 易误用：p值不等于效应大小或因果证明；未拒绝独立性不等于证明完全独立。帮助页中p≥0.05仍写拒绝原假设的句子与其例释矛盾，不能照搬；不把百分比当观测计数。

本地依据：B10248299.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。官方页直接覆盖定类变量的列联表独立性检验；论文的SNP质控、遗传编码、批量检验和关联解释仍需单独设计。

方法边界来源：[SciPy：chi2_contingency的独立性检验及适用条件](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.contingency.chi2_contingency.html)、[statsmodels：多重检验校正](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)。

## M30 二分类Logistic回归与关联参数估计

SPSSPRO：完全对应；[逻辑回归](https://www.spsspro.com/help/logit-regression/)。

输入与前提：二分类结局、基因型/特征编码、参考水平、独立样本标识，以及事先确定的协变量、交互项和缺失处理。 区分统计推断与预测任务；明确logit链接与截距，检查共线性、样本信息不足及完全/近完全分离；不能假定自变量彼此必须独立。

核验：核对收敛与系数稳定性；推断报告系数、OR、区间及检验方法，批量分析考虑多重检验；预测另按G2/G3报告外部区分度与校准。 易误用：OR是优势比，不是风险比或概率变化百分比；显著的似然比检验不能单独证明模型有效、预测可靠或存在因果。帮助页的两类均值近似手算不能当极大似然拟合结果。

本地依据：B10248299.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。基本二分类模型、系数与优势比输出可直接对应；不将人口Logistic增长曲线、SKAT或多分类实现自动并入本条。

方法边界来源：[statsmodels：Logit模型与极大似然拟合](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.html)、[statsmodels：秩亏、分离与似然收敛风险](https://www.statsmodels.org/stable/pitfalls.html)、[statsmodels：多重检验校正](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)。

## M31 空间自相关：Moran’s I

SPSSPRO：未覆盖；本次未核得专项帮助页。

输入与前提：空间单元与连续属性y、对应一致的空间权重矩阵W、坐标/投影及邻接定义、缺失和无邻居单元处理。 预先确定邻接/距离规则及权重标准化；分清全局与局部统计量、空间与时间索引；本地摘要只写Moran’s I，未证明采用了哪种W或推断设定。

核验：检查y与W的顺序一致、权重与孤立单元；报告I值、零假设、随机化次数、单/双侧和所用p值类型，并比较合理邻接定义的敏感性。 易误用：空间集聚不等于因果机制；全局统计量不能直接指出每个局部热点。PySAL的解析p值和置换p值尾部设置不同，不能只写一个不明来源的p值；不能把重复栅格插值当新增独立观测。

本地依据：D24106570027.pdf（原件未随公开包提供，按文件名及所列页码核验），物理第2页，摘要声明。本轮检索空间自相关、Moran、莫兰及空间统计相关词，未核得SPSSPRO专项页；普通Pearson相关帮助不等同空间权重下的自相关。

方法边界来源：[PySAL esda 2.9：Moran空间权重与推断参数](https://pysal.org/esda/v2.9.0/source/generated/esda.Moran.html)。

## 访问限制

BP回归页在本次官方搜索中能读到正文，但直接打开两次返回错误；不宣称已验证实际界面或运行功能。所有软件参数在实际使用时核对当前实现。统计与算法建议是结合方法依据的归纳，不是比赛强制规范。
