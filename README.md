# 中文 aiml 机器人实现

使用结巴分词和修改过的 python aiml 包实现

## 使用

1. 需要 python 2 环境

2. 使用 pip 安装依赖

   ```shell
   pip install textrank4zh
   ```

   执行主程序进行对话

   ```shell
   python main.py
   ```
### 部署网页

如果需要部署网页服务器，还需安装依赖

```shell
pip install web.py
```

   然后运行 application 程序

   ```shell
   python run application.py
   ```

   访问网页 `localhost:8080`




## 编写 AIML

### 自定义词库

在文件 `source/user-dict` 中录入自定义词汇，以避免错误分词：

```
春节联欢晚会 10 n
```

原结巴分词包中，不要求自定义词库的词、词性标注，但是在 textrank4zh 包的实现里，需要有词性标注才能正确使用。

词性标注参见：[词性标记](https://gist.github.com/luw2007/6016931) ，后文给出简表。

*注：自定义词典不要用 Windows 记事本保存*

## 测试关键词提取结果

使用 split-test.py 测试语句分词、提取结果，以确定 pattern 标签中的写作内容。

借助上面的自定义词库，避免一些错误；在 split-test 运行时输入 `reload` ，可以实时更新分词词典。（注意需要在保存已更改的 user-dict 文件后执行命令）

### 替换词汇

基于 aiml 原本实现中的 DefaultSub.py 实现，可进行同义词替换。

比如输入：我喜欢踢足球。根据替换词典中的规则 ['喜欢', '爱']，将语句处理为“我爱踢足球”，可以直接对应到“我爱踢足球”的 pattern 规则，省去多余的 pattern 书写。

因为减少在内存中 Trie 树的空间占用，这种可替换词汇策略应该优于下面的 `简化写作` 考虑使用，但要注意，必须为完全可以相互替代的同义词添加可替换词汇，以避免引起歧义。

### 简化写作

添加了 unfold-shorts.py 文件，该文件将对以下 pattern 内容进行解析（文件名 test.aiml）

```xml
<category>
  <pattern> I
    <fold>
      <or>LIKE</or>
      <or>HATE</or>
    </fold> YOU
  </pattern>
  <template>balabala</template>
</category>
```

解析生成 test-unfold.aiml

```xml
<category>
  <pattern> I LIKE YOU </pattern>
  <template>balabala</template>
</category>
<category>
  <pattern> I HATE YOU </pattern>
  <template>balabala</template>
</category>
```

注意 pattern 标签中的英文内容需要为全大写



#### 附：常用词性标记

| 分类   | 词性         |
| ---- | ---------- |
| a    | 形容词        |
| d    | 副词         |
| e    | 叹词         |
| f    | 方位词        |
| i    | 成语         |
| j    | 简称略语       |
| k    | 后接成份       |
| l    | 习用语（未成为成语） |
| m    | 数词         |
| n    | 名词         |
| p    | 介词         |
| q    | 量词         |
| v    | 动词         |
| y    | 语气词        |

