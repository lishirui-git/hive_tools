price = 0
while price + 10 <= 200:
    strs = ",when (min_build_area > {} and min_build_area <= {}) or  (max_build_area > {} and max_build_area <= {}) then '({},{}]'".format(price, price+10,price,price+10,price,price+10)
    print strs
    price += 10


