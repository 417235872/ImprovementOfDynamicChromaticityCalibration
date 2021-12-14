### 一、绘图代码

- **plot_rawData**

  绘制原始数据方位图像和各方位的数据

- **plot_smoothly**

  绘制高斯滤波和三次样条插值结果

  对于三组结果均做了直方图均衡（或者说：静态色度标定）

  ![滤波](C:\Users\jimbook\Desktop\project\wellPlotAnalyze\image\滤波.png)

- plot_autoAdjustHE

  绘制动态色度标定、平均值法、渐变过渡法和自适应直方图均衡方法的结果

  ![直方图均衡_all](C:\Users\jimbook\Desktop\project\wellPlotAnalyze\image\直方图均衡_all.png)

以下绘图代码已经弃用

- plot_clahe
- plot_dynamicAndReduceBoundary
- plot_gradualChangeWeight
- plot_histogramEqualization
- plot_interpolation
- plot_quicklyAutoAdjust

### 二、数据处理函数

1. 见`./MyTool/dataPrehandle.py`，每个函数均有功能注释
2. **高低频平滑函数**在最终结果中并未使用，结果中使用的平滑函数为**高斯平滑**
3. **自适应法的动态色度标定**函数和**自适应法的动态色度标定\_快速**结果一样，绘图时使用**自适应法的动态色度标定\_快速**

### 三、API--./MyTool/dataPrehandle.py

1.高低频平滑

```python
def smoothlyData(data:pd.DataFrame)
```

- 输入参数

| 变量名 | type             | 说明                                                         |
| ------ | ---------------- | ------------------------------------------------------------ |
| data   | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要求 |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签与输入值相同

2.高斯平滑

```python
def gaussianFilter(data:pd.DataFrame,sigma=3)
```

- 输入参数

| 变量名 | type             | 说明                                                         |
| ------ | ---------------- | ------------------------------------------------------------ |
| data   | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要求 |
| sigma  | int              | 高斯核函数的标准差                                           |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签与输入值相同

3.角度方向插值

```python
def interpolation(data:pd.DataFrame,kind="cubic",tarNumb=720)
```

- 输入参数

| 变量名    | type                                   | 说明                                                         |
| --------- | -------------------------------------- | ------------------------------------------------------------ |
| data      | pandas.DataFrame                       | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要求 |
| kind      | “linear”、“quadratic”、"cubic"中的一个 | 插值方法：“linear”：线性插值；“quadratic”：二阶样条插值；"cubic"：三次样条插值 |
| tarNumber | int                                    | 插值后的列数                                                 |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签变为角度值（单位：°，从0°到360°）

4.直方图均衡

```python
def histogramEqualization(data:pd.DataFrame)
```

- 输入参数

| 变量名 | type             | 说明                                                         |
| ------ | ---------------- | ------------------------------------------------------------ |
| data   | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要求 |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签与输入值相同

5.变换函数：直方图均衡

```python
def transform_HE(data:pd.DataFrame)
```

- 输入参数

| 变量名 | type             | 说明                                                         |
| ------ | ---------------- | ------------------------------------------------------------ |
| data   | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要求 |

- 返回值
  - type：function
  - 返回一个直方图变换函数function(x)，等同于参数确定的`histogramEqualization(data:pd.DataFrame)`

6.动态应用函数

```python
def dynamicOperation(data:pd.DataFrame,function: callable,winlen=300)
```

- 输入参数

| 变量名   | type             | 说明                                                         |
| -------- | ---------------- | ------------------------------------------------------------ |
| data     | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要 |
| function | callable(函数)   | 处理每一个数据窗数据的函数（如`histogramEqualization(data:pd.DataFrame)`） |
| winlen   | int              | 窗长                                                         |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签与输入值相同

7.平均值法的动态色度标定

```python
def dynamicOperation_MeanValue(data:pd.DataFrame,function: callable,winlen=300)
```

- 输入参数

| 变量名   | type             | 说明                                                         |
| -------- | ---------------- | ------------------------------------------------------------ |
| data     | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要 |
| function | callable(函数)   | 处理每一个数据窗数据的函数（如`histogramEqualization(data:pd.DataFrame)`） |
| winlen   | int              | 窗长                                                         |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签与输入值相同

8.渐变平滑法的动态色度标定

```python
def dynamicOperation_GradualChange(data:pd.DataFrame,function, winlen:int = 300)
```

- 输入参数

| 变量名   | type             | 说明                                                         |
| -------- | ---------------- | ------------------------------------------------------------ |
| data     | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要 |
| function | callable(函数)   | 处理每一个数据窗数据的函数（如`histogramEqualization(data:pd.DataFrame)`） |
| winlen   | int              | 窗长                                                         |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签与输入值相同

9.自适应法的动态色度标定

```python
def dynamicOperation_AutoAdjust(data:pd.DataFrame,function, winlen:int = 300)
```

- 输入参数

| 变量名   | type             | 说明                                                         |
| -------- | ---------------- | ------------------------------------------------------------ |
| data     | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要 |
| function | callable(函数)   | 处理每一个数据窗数据的函数（如`histogramEqualization(data:pd.DataFrame)`） |
| winlen   | int              | 窗长                                                         |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签与输入值相同

10.自适应法的动态色度标定_快速

```python
def dynamicOperation_QuicklyAutoAdjust(data:pd.DataFrame,transform_function, winlen:int = 300)
```

- 输入参数

| 变量名             | type             | 说明                                                         |
| ------------------ | ---------------- | ------------------------------------------------------------ |
| data               | pandas.DataFrame | index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签不做要 |
| transform_function | callable(函数)   | 要求接收一个参数data，返回处理每一个深度点数据的函数（如`transform_HE(data:pd.DataFrame)`） |
| winlen             | int              | 窗长                                                         |

- 返回值
  - **type：**pandas.DataFrame
  - index为深度值，标签为“DEPTH”；每一列为不同方位的数据，列标签与输入值相同