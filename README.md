# self-refine

### 环境配置

```bash
pip install rpy2.robjects difflib scipy pandas
```

### Setup

```bash
export API_KEY=
export BASE_URL=
export PYTHONPATH=".:../:.:src:../:../../:.:prompt-lib"
```

### **Getting Started with PIE**

- **代码输入**：在`run.py`的`test()`中输入`slow_code`

```bash
python -u src/pie/run.py test
```

- **文件测试**

```bash
python -u src/pie/run.py test_f
```

- **自定义文件**

```bash
python -u src/pie/run.py --slow_programs_file {slow_program_path} --max_attempts 4 --outfile {output_path} --feedback_type rich

#—max_attempts 代表迭代次数
#--feedback_type naive的feedback为"It could be faster";none无feedback;其他的feedback为"Why is this code slow?"

```

<aside>
💡

原数据示例为python，第一次返回结果可能出错—可以重复运行or更换数据集

</aside>