def sanitize_input(param, param_type, default_value):
    """正規化傳入的參數

    Args:
        param: 傳入的參數值
        param_type: 該參數應該是什麼類型，比方 int
        default_value: 若無法轉型成 param_type，預設回傳值

    Returns:
        回傳正規化後的值
    """
    try:
        return param_type(param)
    except:
        return default_value
