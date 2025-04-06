import akshare as ak
def get_stock_code(stock_name: str, market: str = "A") -> str:
    try:
        # 根据市场获取数据
        if market == "A":
            df = ak.stock_zh_a_spot()
            code_col, name_col = "代码", "名称"
        elif market == "HK":
            df = ak.stock_hk_spot()
            code_col, name_col = "代码", "名称"
        elif market == "US":
            df = ak.stock_us_spot()
            code_col, name_col = "代码", "名称"
        else:
            raise ValueError("不支持的 market 参数，可选值：'A'/'HK'/'US'")

        # 精确匹配查询
        matched = df[df[name_col].str.strip() == stock_name.strip()]

        if not matched.empty:
            return matched.iloc[0][code_col]
        else:
            return None

    except Exception as e:
        print(f"查询失败：{str(e)}")
        return None
def get_stock_name(stock_code: str, market: str = "A") -> str:
    try:
        # 根据市场获取数据
        if market == "A":
            df = ak.stock_zh_a_spot()
            code_col, name_col = "代码", "名称"
        elif market == "HK":
            df = ak.stock_hk_spot()
            code_col, name_col = "代码", "名称"
        elif market == "US":
            df = ak.stock_us_spot()
            code_col, name_col = "代码", "名称"
        else:
            raise ValueError("不支持的 market 参数，可选值：'A'/'HK'/'US'")

        # 精确匹配查询
        matched = df[df[code_col].str.strip() == stock_code.strip()]

        if not matched.empty:
            return matched.iloc[0][name_col]
        else:
            return None

    except Exception as e:
        print(f"查询失败：{str(e)}")
        return None