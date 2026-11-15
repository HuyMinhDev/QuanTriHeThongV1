# Trích đoạn ngắn đã đọc qua web, không phải toàn bộ source tác giả.
# Nguồn chính xác và phạm vi ở SOURCE.md.
def concave_func(x, t):
    return x**(1-t)

def distance_concave_func(x_anchor, x, t):
    return (concave_func(x_anchor,t)-concave_func(x,t))*(1-t)*(x**(-t))
