import numpy as np
import pandas as pd
from scipy.optimize import minimize
import warnings

warnings.filterwarnings("ignore")


class ESGModel:
    """
    ESG评分模型
    基于甲模型设计理念实现的企业ESG评分系统
    """

    def __init__(self, custom_params=None):
        # 默认行业权重配置（基于甲模型实质性原则）
        self.default_industry_weights = {
            "能源": {"E": 0.5, "S": 0.25, "G": 0.25},
            "金融": {"E": 0.2, "S": 0.35, "G": 0.45},
            "科技": {"E": 0.25, "S": 0.4, "G": 0.35},
            "制造": {"E": 0.4, "S": 0.35, "G": 0.25},
            "制造业": {"E": 0.4, "S": 0.35, "G": 0.25},
            "消费": {"E": 0.3, "S": 0.4, "G": 0.3},
            "默认": {"E": 0.33, "S": 0.33, "G": 0.34},
        }

        # 可自定义的参数配置
        self.params = {
            # 权重相关参数
            "alpha": 0.5,  # 主观权重系数
            "industry_weights": self.default_industry_weights.copy(),
            # 交叉项系数（基于甲模型整合性原则）
            "cross_term_coeffs": {
                "delta": 0.1,  # E×S交叉项系数
                "epsilon": 0.15,  # E×G交叉项系数
                "zeta": 0.12,  # S×G交叉项系数
            },
            # 非线性调整参数
            "nonlinear_params": {
                "severity_factor": 0.4,  # 严重度放大因子β
                "max_bonus": 10,  # 最大加分值
                "bonus_steepness": 0.7,  # 奖励曲线陡度k
                "threshold_multiplier": 1.0,  # 阈值调节系数
            },
            # 事件类型系数λ（基于甲模型动态适应性）
            "event_coeffs": {
                "数据泄露": 1.2,
                "工伤事故": 0.8,
                "环境污染": 1.5,
                "财务舞弊": 1.3,
                "劳工纠纷": 0.9,
                "产品质量": 1.1,
                "供应链风险": 0.9,
                "合规违规": 1.4,
            },
            # 政策响应参数（基于甲模型动态适应性）
            "policy_response": {
                "carbon_tax_sensitivity": 0.05,  # 碳税敏感系数
                "esg_disclosure_weight": 1.0,  # ESG披露权重
                "green_finance_bonus": 0.1,  # 绿色金融加分系数
            },
        }

        # 如果提供了自定义参数，则更新
        if custom_params:
            self._update_params(custom_params)

        # 保持向后兼容
        self.industry_weights = self.params["industry_weights"]

        # 行业名称映射
        self.industry_mapping = {
            "制造业": "制造",
            "能源行业": "能源",
            "金融业": "金融",
            "科技行业": "科技",
            "消费行业": "消费",
        }

        # 定义ESG指标分类 - 基于甲模型附录
        self.e_indicators = [
            "碳排放总量",
            "范围1直接排放",
            "范围2间接排放",
            "范围3价值链排放",
            "单位营收能耗",
            "可再生能源占比",
            "水资源循环利用率",
            "危险废物处置合规率",
            "温室气体减排量",
            "碳排放权交易履约率",
            "环保行政处罚次数",
        ]

        self.s_indicators = [
            "员工流失率（核心岗位）",
            "残疾人就业比例",
            "客户隐私保护认证情况",
            "突发公共卫生事件应急响应效率",
            "员工培训覆盖率",
            "职业健康安全事故率",
            "供应链ESG审核比例",
            "中小企业账款逾期率",
            "乡村振兴投入金额",
            "公益捐赠占净利润比例",
        ]

        self.g_indicators = [
            "产品质量投诉处理时效",
            "数据安全事件发生次数",
            "供应链本地化率",
            "行业协会ESG评级",
            "供应链ESG风险应急预案完备性",
            "气候风险压力测试覆盖率",
            "ESG目标与战略匹配度",
            "小股东提案通过率",
            "ESG指标与国际标准对标",
            "独立董事比例",
            "反商业贿赂培训覆盖率",
            "ESG绩效纳入高管薪酬比例",
            "利益相关方沟通频率",
            "绿色债券发行规模占比",
            "ESG报告第三方鉴证比例",
            "内幕信息知情人管理规范完备性",
            "党建引领ESG工作成效",
            "董事会ESG委员会设立情况",
        ]

        # 定义负向指标（越小越好）
        self.negative_indicators = {
            "碳排放总量",
            "范围1直接排放",
            "范围2间接排放",
            "范围3价值链排放",
            "单位营收能耗",
            "员工流失率（核心岗位）",
            "职业健康安全事故率",
            "中小企业账款逾期率",
            "产品质量投诉处理时效",
            "数据安全事件发生次数",
            "环保行政处罚次数",
        }

        # 保持向后兼容的属性
        self.event_coefficients = self.params["event_coeffs"]
        self.severity_factor = self.params["nonlinear_params"]["severity_factor"]

    def _update_params(self, custom_params):
        """
        更新模型参数（支持嵌套字典更新）
        """

        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if (
                    isinstance(value, dict)
                    and key in base_dict
                    and isinstance(base_dict[key], dict)
                ):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value

        # 确保 custom_params 是字典类型
        if not isinstance(custom_params, dict):
            print(f"警告：传入的参数不是字典类型，而是 {type(custom_params)}，跳过更新")
            return

        deep_update(self.params, custom_params)

        # 更新向后兼容属性，并确保类型正确
        if "industry_weights" in self.params and isinstance(
            self.params["industry_weights"], dict
        ):
            self.industry_weights = self.params["industry_weights"]
        if "event_coeffs" in self.params and isinstance(
            self.params["event_coeffs"], dict
        ):
            self.event_coefficients = self.params["event_coeffs"]
        if "nonlinear_params" in self.params and isinstance(
            self.params["nonlinear_params"], dict
        ):
            self.severity_factor = self.params["nonlinear_params"].get(
                "severity_factor", 0.4
            )

    def update_parameters(self, **kwargs):
        """
        动态更新模型参数的公共接口
        """
        self._update_params(kwargs)

    def get_parameter_info(self):
        """
        获取当前参数配置信息
        """
        return {
            "主观权重系数α": self.params["alpha"],
            "交叉项系数": self.params["cross_term_coeffs"],
            "非线性调整参数": self.params["nonlinear_params"],
            "事件类型系数": self.params["event_coeffs"],
            "政策响应参数": self.params["policy_response"],
        }

    def preprocess_data(self, data):
        """
        数据预处理：处理缺失值、异常值和标准化
        """
        processed_data = data.copy()

        # 1. 缺失值处理
        for column in processed_data.columns:
            if processed_data[column].dtype in ["float64", "int64"]:
                # 数值型：用中位数填充
                processed_data[column].fillna(
                    processed_data[column].median(), inplace=True
                )
            else:
                # 分类型：用众数填充
                processed_data[column].fillna(
                    processed_data[column].mode()[0]
                    if not processed_data[column].mode().empty
                    else "Unknown",
                    inplace=True,
                )

        # 2. 异常值处理（使用IQR方法）
        for column in processed_data.select_dtypes(include=[np.number]).columns:
            Q1 = processed_data[column].quantile(0.25)
            Q3 = processed_data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # 缩尾处理
            processed_data[column] = np.clip(
                processed_data[column], lower_bound, upper_bound
            )

        # 3. 数据标准化（考虑负向指标）
        numeric_columns = processed_data.select_dtypes(include=[np.number]).columns

        # 检查是否只有一行数据
        if len(processed_data) == 1:
            # 对于单行数据，使用基于指标理想值的标准化
            for column in numeric_columns:
                value = processed_data[column].iloc[0]
                if column in self.negative_indicators:
                    # 负向指标：值越小越好，理想值为0，最大容忍值为100
                    processed_data[column] = max(0, (100 - value) / 100)
                else:
                    # 正向指标：值越大越好，理想值为100，最小值为0
                    processed_data[column] = max(0, min(1, value / 100))
        else:
            # 多行数据使用原有的标准化方法
            for column in numeric_columns:
                # 负向指标需要反向处理
                if column in self.negative_indicators:
                    # 对于负向指标，值越小越好，所以需要反向
                    max_val = processed_data[column].max()
                    min_val = processed_data[column].min()
                    if max_val != min_val:
                        processed_data[column] = (max_val - processed_data[column]) / (
                            max_val - min_val
                        )
                    else:
                        processed_data[column] = 0.5
                else:
                    # 正向指标，值越大越好
                    min_val = processed_data[column].min()
                    max_val = processed_data[column].max()
                    if max_val != min_val:
                        processed_data[column] = (processed_data[column] - min_val) / (
                            max_val - min_val
                        )
                    else:
                        processed_data[column] = 0.5  # 如果所有值相同，设为中间值

        return processed_data

    def calculate_vif(self, data):
        """
        计算方差膨胀因子(VIF)检测多重共线性
        """

        vif_data = pd.DataFrame()
        vif_data["Feature"] = data.columns
        vif_data["VIF"] = [
            self._calculate_single_vif(data, i) for i in range(data.shape[1])
        ]

        return vif_data

    def _calculate_single_vif(self, data, feature_idx):
        """
        计算单个特征的VIF值
        """
        try:
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import r2_score

            X = data.drop(data.columns[feature_idx], axis=1)
            y = data.iloc[:, feature_idx]

            if X.shape[1] == 0:
                return 1.0

            model = LinearRegression()
            model.fit(X, y)
            y_pred = model.predict(X)
            r2 = r2_score(y, y_pred)

            if r2 >= 0.999:  # 避免除零错误
                return float("inf")

            vif = 1 / (1 - r2)
            return vif
        except Exception:
            return 1.0

    def calculate_ahp_weights(self, comparison_matrix):
        """
        计算AHP主观权重
        """
        # 计算几何平均
        n = comparison_matrix.shape[0]
        geometric_means = np.power(np.prod(comparison_matrix, axis=1), 1 / n)

        # 归一化得到权重
        weights = geometric_means / np.sum(geometric_means)

        # 一致性检验
        lambda_max = np.sum(np.dot(comparison_matrix, weights) / weights) / n
        ci = (lambda_max - n) / (n - 1)
        ri_values = {3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
        ri = ri_values.get(n, 1.0)
        cr = ci / ri if ri > 0 else 0

        return weights, cr

    def calculate_entropy_weights(self, data):
        """
        计算熵权法客观权重
        """
        # 数据归一化
        data_sum = data.sum(axis=0)
        # 避免除零错误
        data_sum = data_sum.replace(0, 1e-10)
        data_normalized = data / data_sum

        # 计算熵值
        m, n = data_normalized.shape
        entropy = np.zeros(n)

        for j in range(n):
            p = data_normalized.iloc[:, j]
            p = p[p > 0]  # 避免log(0)
            if len(p) > 0:
                entropy[j] = -np.sum(p * np.log(p)) / np.log(m)
            else:
                entropy[j] = 0

        # 引入变异系数修正 - 修复NaN问题
        data_std = data.std()
        data_mean = data.mean()

        # 避免除零错误和NaN
        cv = np.where(
            (data_mean != 0) & (~np.isnan(data_std)) & (data_std != 0),
            data_std / data_mean,
            1.0,
        )  # 如果标准差为0或均值为0，设置变异系数为1

        g = cv * (1 - entropy)  # 修正后的权重指标

        # 避免所有权重为0的情况
        if g.sum() == 0 or np.isnan(g.sum()):
            # 如果所有权重都是0或NaN，使用均匀权重
            weights = pd.Series(np.ones(n) / n, index=data.columns)
        else:
            # 归一化权重
            weights = g / g.sum()

        return weights.values

    def combine_weights(self, subjective_weights, objective_weights, alpha=0.5):
        """
        组合赋权法：结合主观权重和客观权重
        """

        def objective_function(w):
            return alpha * np.sum((w - subjective_weights) ** 2) + (1 - alpha) * np.sum(
                (w - objective_weights) ** 2
            )

        # 约束条件：权重和为1
        constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
        bounds = [(0, 1) for _ in range(len(subjective_weights))]

        # 初始值
        initial_weights = (subjective_weights + objective_weights) / 2

        # 优化求解
        result = minimize(
            objective_function,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        return result.x if result.success else initial_weights

    def calculate_factor_scores(self, data, weights):
        """
        计算E、S、G因子得分
        """
        # 根据指标名称分配到各因子
        e_indices = [
            i for i, col in enumerate(data.columns) if col in self.e_indicators
        ]
        s_indices = [
            i for i, col in enumerate(data.columns) if col in self.s_indicators
        ]
        g_indices = [
            i for i, col in enumerate(data.columns) if col in self.g_indicators
        ]

        # 计算各因子得分
        e_score = (
            np.sum(data.iloc[:, e_indices] * weights[e_indices], axis=1)
            if e_indices
            else pd.Series([0] * len(data))
        )
        s_score = (
            np.sum(data.iloc[:, s_indices] * weights[s_indices], axis=1)
            if s_indices
            else pd.Series([0] * len(data))
        )
        g_score = (
            np.sum(data.iloc[:, g_indices] * weights[g_indices], axis=1)
            if g_indices
            else pd.Series([0] * len(data))
        )

        # 检查是否为单行数据
        if len(data) == 1:
            # 对于单行数据，直接将加权得分转换为0-100分
            e_score = e_score * 100
            s_score = s_score * 100
            g_score = g_score * 100
        else:
            # 多行数据使用原有的标准化方法
            # 标准化到0-100分
            if e_score.max() != e_score.min():
                e_score = (
                    (e_score - e_score.min()) / (e_score.max() - e_score.min()) * 100
                )
            else:
                e_score = pd.Series([50] * len(data))

            if s_score.max() != s_score.min():
                s_score = (
                    (s_score - s_score.min()) / (s_score.max() - s_score.min()) * 100
                )
            else:
                s_score = pd.Series([50] * len(data))

            if g_score.max() != g_score.min():
                g_score = (
                    (g_score - g_score.min()) / (g_score.max() - g_score.min()) * 100
                )
            else:
                g_score = pd.Series([50] * len(data))

        return e_score, s_score, g_score

    def calculate_base_score(self, e_score, s_score, g_score, industry="默认"):
        """
        计算Base Score（显式交叉项法）
        基于甲模型整合性原则，考虑E、S、G维度的联动效应
        """
        # 处理行业名称映射
        mapped_industry = self.industry_mapping.get(industry, industry)

        # 获取行业权重，如果不存在则使用默认权重
        if mapped_industry in self.params["industry_weights"]:
            weights = self.params["industry_weights"][mapped_industry]
        else:
            print(f"警告：未找到行业'{industry}'的权重配置，使用默认权重")
            weights = self.params["industry_weights"]["默认"]

        alpha, beta, gamma = weights["E"], weights["S"], weights["G"]

        # 获取可配置的交叉项系数
        cross_coeffs = self.params["cross_term_coeffs"]
        delta = cross_coeffs["delta"]  # E×S交叉项系数
        epsilon = cross_coeffs["epsilon"]  # E×G交叉项系数
        zeta = cross_coeffs["zeta"]  # S×G交叉项系数

        # 显式交叉项法计算Base Score
        # 基础得分：线性组合
        linear_score = alpha * e_score + beta * s_score + gamma * g_score

        # 交叉项得分：捕捉维度间协同效应
        cross_score = (
            delta * (e_score * s_score / 100)
            + epsilon * (e_score * g_score / 100)
            + zeta * (s_score * g_score / 100)
        )

        base_score = linear_score + cross_score

        return base_score

    def apply_nonlinear_adjustments(self, base_score, events=None):
        """
        应用非线性调整（基于甲模型非线性事件调整原则）
        包括事件分级惩罚、饱和函数加分、指标交互项调整
        """
        adjusted_score = (
            base_score.copy() if hasattr(base_score, "copy") else base_score
        )

        # 获取非线性调整参数
        nl_params = self.params["nonlinear_params"]
        event_coeffs = self.params["event_coeffs"]

        if events is not None and len(events) > 0:
            # 事件分级惩罚模型
            for event in events:
                # 跳过空列表或非字典类型的事件
                if not isinstance(event, dict) or len(event) == 0:
                    continue

                event_type = event.get("type", "其他")
                severity = event.get("severity", 1)  # 1-5级严重度

                # 获取事件类型系数λ_k
                lambda_k = event_coeffs.get(event_type, 1.0)

                # 严重度放大因子β
                beta = nl_params["severity_factor"]

                # 事件惩罚：λ_k × e^(β × Severity_k)
                penalty = lambda_k * np.exp(beta * severity)

                # 应用惩罚（确保不会产生负分）
                if hasattr(adjusted_score, "__iter__"):
                    adjusted_score = np.maximum(adjusted_score - penalty, 0)
                else:
                    adjusted_score = max(adjusted_score - penalty, 0)

        # 饱和函数加分法（对优秀表现的奖励）
        if hasattr(base_score, "__iter__"):
            # 对于高分企业给予额外奖励（避免过度加分）
            high_performers = base_score > 80
            if np.any(high_performers):
                max_bonus = nl_params["max_bonus"]
                k = nl_params["bonus_steepness"]
                threshold = 80 * nl_params["threshold_multiplier"]

                # 饱和函数：MaxBonus / (1 + e^(-k × (Performance - Threshold)))
                performance_above_threshold = base_score[high_performers] - threshold
                bonus = max_bonus / (1 + np.exp(-k * performance_above_threshold))
                adjusted_score[high_performers] += bonus
        else:
            # 单个分数的处理
            if base_score > 80:
                max_bonus = nl_params["max_bonus"]
                k = nl_params["bonus_steepness"]
                threshold = 80 * nl_params["threshold_multiplier"]

                performance_above_threshold = base_score - threshold
                bonus = max_bonus / (1 + np.exp(-k * performance_above_threshold))
                adjusted_score += bonus

        # 确保分数在合理范围内（0-100）
        if hasattr(adjusted_score, "__iter__"):
            adjusted_score = np.clip(adjusted_score, 0, 100)
        else:
            adjusted_score = max(0, min(adjusted_score, 100))

        return adjusted_score

    def calculate_esg_score(
        self,
        data,
        industry="默认",
        events=None,
        subjective_weights=None,
        alpha=0.5,
        jia_model_params=None,
    ):
        """
        计算完整的ESG评分（基于甲模型设计理念）
        """
        # 应用甲模型参数（如果提供）
        if jia_model_params is not None:
            self.update_parameters(**jia_model_params)
            # 如果甲模型参数中包含alpha，使用它
            if "alpha" in jia_model_params:
                alpha = jia_model_params["alpha"]

        # 1. 数据预处理
        processed_data = self.preprocess_data(data)

        # 2. 权重计算
        if subjective_weights is None:
            # 使用甲模型的行业差异化权重
            # 确保industry_weights是字典类型
            if not isinstance(self.params["industry_weights"], dict):
                print(
                    f"错误：industry_weights应该是字典类型，但得到了{type(self.params['industry_weights'])}"
                )
                # 使用默认权重
                self.params["industry_weights"] = self.default_industry_weights.copy()

            # 获取行业权重
            industry_weights = self.params["industry_weights"].get(industry)
            if industry_weights is None:
                # 如果没有找到对应行业，使用默认权重
                industry_weights = self.params["industry_weights"].get("默认")
                if industry_weights is None:
                    # 如果连默认权重都没有，创建一个
                    industry_weights = {"E": 0.33, "S": 0.33, "G": 0.34}

            # 确保获取到的权重也是字典类型
            if not isinstance(industry_weights, dict):
                print(f"错误：行业权重应该是字典类型，但得到了{type(industry_weights)}")
                # 使用默认权重
                industry_weights = {"E": 0.33, "S": 0.33, "G": 0.34}

            # 确保权重包含必需的键
            if not all(key in industry_weights for key in ["E", "S", "G"]):
                print(f"错误：行业权重缺少必需的键，当前权重：{industry_weights}")
                industry_weights = {"E": 0.33, "S": 0.33, "G": 0.34}

            subjective_weights = np.array(
                [industry_weights["E"], industry_weights["S"], industry_weights["G"]]
            )
            # 扩展到所有指标
            n_indicators = processed_data.shape[1]
            e_indicators = n_indicators // 3
            s_indicators = n_indicators // 3
            g_indicators = n_indicators - e_indicators - s_indicators

            expanded_weights = np.concatenate(
                [
                    np.full(e_indicators, subjective_weights[0] / e_indicators),
                    np.full(s_indicators, subjective_weights[1] / s_indicators),
                    np.full(g_indicators, subjective_weights[2] / g_indicators),
                ]
            )
            subjective_weights = expanded_weights

        objective_weights = self.calculate_entropy_weights(processed_data)
        final_weights = self.combine_weights(
            subjective_weights, objective_weights, alpha
        )

        # 3. 因子得分计算
        e_score, s_score, g_score = self.calculate_factor_scores(
            processed_data, final_weights
        )

        # 4. Base Score计算（使用甲模型交叉项）
        base_score = self.calculate_base_score(e_score, s_score, g_score, industry)

        # 5. 非线性调整（甲模型事件分级惩罚）
        final_score = self.apply_nonlinear_adjustments(base_score, events)

        # 6. 政策响应调整（甲模型动态适应性）
        if jia_model_params and "policy_params" in jia_model_params:
            policy_params = jia_model_params["policy_params"]
            # 应用政策响应调整
            policy_adjustment = (
                policy_params.get("carbon_tax_sensitivity", 0)
                * e_score
                * 0.1  # 碳税影响
                + policy_params.get("esg_disclosure_weight", 0) * 5  # 披露质量奖励
                + policy_params.get("green_finance_bonus", 0) * 10  # 绿色金融奖励
            )
            final_score = final_score + policy_adjustment * policy_params.get(
                "regulatory_compliance", 1.0
            )

        # 确保分数在合理范围内
        if hasattr(final_score, "__iter__"):
            final_score = np.clip(final_score, 0, 100)
        else:
            final_score = max(0, min(final_score, 100))

        # 返回详细结果
        results = {
            "final_score": final_score,
            "base_score": base_score,
            "e_score": e_score,
            "s_score": s_score,
            "g_score": g_score,
            "weights": final_weights,
            "processed_data": processed_data,
            "jia_model_params": jia_model_params or {},
        }

        return results

    def get_score_interpretation(self, score):
        """
        ESG评分解释
        """
        if score >= 80:
            return "优秀", "ESG表现卓越，可持续发展能力强"
        elif score >= 60:
            return "良好", "ESG表现较好，具备一定可持续发展能力"
        elif score >= 40:
            return "一般", "ESG表现中等，需要改进部分领域"
        else:
            return "较差", "ESG表现不佳，存在较大风险，需要全面改进"
