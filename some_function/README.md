## URM程序完成情况

| 序号 | 内容                                                        | 实现 | 备注                                       |
|------|-----------------------------------------------------------|--|------------------------------------------|
| 01   | plus(x, y) = x + y                                         | ✅ |                                          |
| 02   | mult(x, y) = x * y                                         | ✅ |                                          |
| 03   | pow(x, 0) = 1 and pow(x, y + 1) = pow(x, y) * x            |  | 太难了, 出现概率不大                              |
| 04   | pred(0) = 0 and pred(x + 1) = x                            | ✅ |                                          |
| 05   | minus(x, y) = 0 whenever x < y and minus(x, y) = x - y     | ✅ |                                          |
| 06   | sg(0) = 0 and sg(x) = 1 for other x                        | ✅ |                                          |
| 07   | isg(0) = 1 and isg(x) = 0 for other x                      | ✅ |                                          |
| 08   | lt(x, y) = 0 if x < y and lt(x, y) = 1 for other x and y   | ✅ | 两种返回结果均实现                                |
| 09   | eq(x, y) = 0 if x = y and eq(x, y) = 1 for other x and y   | ✅| 两种返回结果均实现                                |
| 10   | gt(x, y) = 0 if x > y and gt(x, y) = 1 for other x and y   | ✅ | 两种返回结果均实现                                |
| 11   | dist(x, y) = minus(x, y) + minus(y, x)                     |  | 当URM只涉及自然数范围时，实现这个函数意义好像不大，因为两个减部必然有一个为0 |
| 12   | 0! = 1 and (x + 1)! = x! * (x + 1)                         |  | 太难了, 出现概率不大                              |
| 13   | min(x, y) is the minimum of x and y                        | ✅ |                                          |
| 14   | max(x, y) is the maximum of x and y                        | ✅ |                                          |
| 15   | K(x, y) = (x + y) * (x + y + 1) / 2 + y                     |  | 太难了, 出现概率不大                              |
