import numpy as np
import pandas as pd


class ESGDataProcessor:
    """
    ESG数据处理器
    用于处理真实的ESG指标数据
    """

    def __init__(self):
        pass

        # 环境指标 (E) - 基于甲模型附录
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

        # 社会指标 (S) - 基于甲模型附录
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

        # 治理指标 (G) - 基于甲模型附录
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

        # 支持的行业类型
        self.supported_industries = [
            "制造业",
            "金融业",
            "科技业",
            "能源业",
            "消费业",
            "房地产业",
            "医疗健康",
            "交通运输",
            "零售业",
            "其他",
        ]

    def validate_company_data(self, data):
        """
        验证公司ESG数据的完整性和有效性
        """
        required_columns = ["company_name", "industry"]
        missing_columns = [col for col in required_columns if col not in data.columns]

        if missing_columns:
            raise ValueError(f"缺少必要列: {missing_columns}")

        # 验证行业是否在支持列表中
        invalid_industries = data[~data["industry"].isin(self.supported_industries)][
            "industry"
        ].unique()
        if len(invalid_industries) > 0:
            print(f"警告: 发现不在支持列表中的行业: {invalid_industries}")

        return True

    def clean_and_standardize_data(self, data):
        """
        清洗和标准化ESG数据
        """
        cleaned_data = data.copy()

        # 标准化列名映射
        column_mapping = {
            "公司名称": "company_name",
            "企业名称": "company_name",
            "公司": "company_name",
            "行业": "industry",
            "行业类型": "industry",
            "所属行业": "industry",
        }

        # 应用列名映射
        for chinese_col, english_col in column_mapping.items():
            if (
                chinese_col in cleaned_data.columns
                and english_col not in cleaned_data.columns
            ):
                cleaned_data = cleaned_data.rename(columns={chinese_col: english_col})

        # 处理缺失值
        numeric_columns = cleaned_data.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in cleaned_data.columns:
                # 用中位数填充数值型缺失值
                cleaned_data[col].fillna(cleaned_data[col].median(), inplace=True)

        # 处理异常值（使用IQR方法）
        for col in numeric_columns:
            if col in cleaned_data.columns:
                Q1 = cleaned_data[col].quantile(0.25)
                Q3 = cleaned_data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                # 将异常值限制在合理范围内
                cleaned_data[col] = cleaned_data[col].clip(lower_bound, upper_bound)

        return cleaned_data

    def get_all_indicators(self):
        """
        获取所有ESG指标列表
        """
        return {"E": self.e_indicators, "S": self.s_indicators, "G": self.g_indicators}

    def get_indicator_info(self, indicator_name):
        """
        获取指定指标的详细信息
        """
        all_indicators = self.get_all_indicators()

        for category, indicators in all_indicators.items():
            if indicator_name in indicators:
                return {
                    "category": category,
                    "name": indicator_name,
                    "full_name": f"{category}类指标 - {indicator_name}",
                }

        return None

    def load_data_from_csv(self, file_path):
        """
        从CSV文件加载ESG数据
        """
        try:
            data = pd.read_csv(file_path)
            self.validate_company_data(data)
            return self.clean_and_standardize_data(data)
        except Exception as e:
            raise ValueError(f"数据加载失败: {str(e)}")

    def export_data_template(self, file_path):
        """
        导出ESG数据模板
        """
        all_indicators = self.get_all_indicators()
        columns = ["company_name", "industry"]

        # 添加所有ESG指标列
        for category_indicators in all_indicators.values():
            columns.extend(category_indicators)

        # 创建空的DataFrame模板
        template_df = pd.DataFrame(columns=columns)
        template_df.to_csv(file_path, index=False, encoding="utf-8-sig")

        return f"数据模板已导出到: {file_path}"


# 使用示例
if __name__ == "__main__":
    processor = ESGDataProcessor()

    # 获取所有ESG指标
    indicators = processor.get_all_indicators()
    print("ESG指标体系:")
    for category, indicator_list in indicators.items():
        print(f"\n{category}类指标 ({len(indicator_list)}个):")
        for i, indicator in enumerate(indicator_list, 1):
            print(f"  {i}. {indicator}")

    # 导出数据模板
    template_path = "esg_data_template.csv"
    result = processor.export_data_template(template_path)
    print(f"\n{result}")

    print("\n支持的行业类型:")
    for i, industry in enumerate(processor.supported_industries, 1):
        print(f"  {i}. {industry}")
