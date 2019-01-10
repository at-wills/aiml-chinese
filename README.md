# 中文 aiml 机器人实现

使用结巴分词和修改过的 python2 aiml 包实现

## 1. 使用

1. 需要 python 2 环境

2. 使用 pip 安装依赖

   ```shell
   pip install textrank4zh
   ```

   执行主程序进行对话

   ```shell
   python main.py
   ```
### 1.1 部署网页

如果需要部署网页服务器，还需安装依赖

```shell
pip install web.py
```

   然后运行 application 程序

   ```shell
   python run application.py
   ```

   访问网页 `localhost:8080`




## 2. 编写 AIML

### 2.1 自定义词库

在文件 `source/user-dict` 中录入自定义词汇，以避免错误分词：

```
春节联欢晚会 10 n
```

原结巴分词包中，不要求自定义词库的词、词性标注，但是在 textrank4zh 包的实现里，需要有词性标注才能正确使用。

词性标注参见：[词性标记](https://gist.github.com/luw2007/6016931) 。最常用的词性为名词，标注为“n”。

*注：自定义词典不要用 Windows 记事本保存*

### 2.2 测试关键词提取结果

使用 split-test.py 测试语句分词、提取结果，以确定 pattern 标签中的写作内容。

借助上面的自定义词库，避免一些错误；在 split-test 运行时输入 `reload` ，可以实时更新分词词典。（注意需要在保存已更改的 user-dict 文件后执行命令）

### 2.3 同义词替换

去除了原 aiml 实现中的 DefaultSubs.py 和 WordSub.py，添加了文件 Sub.py 来实现功能。

需要进行替换的词汇保存在 `source/subs` 中，格式为 `原词 替换词` 。

比如输入：“我喜欢踢球”，关键词提取得到“我 喜欢 踢球”。根据替换词典中的规则 [喜欢 爱]，替换为“我 爱 踢球”，对应到“我 爱 踢球”的 pattern 规则，省去多余的 pattern 书写。

因为减少 Trie 树的体积，这种可替换词汇策略应该优于下面的 `简化写作` 考虑使用。

但要注意：必须为完全可以相互替代的同义词添加可替换词汇，以避免引起歧义，造成后续出错。

### 2.4 简化写作

添加了 unfold_shorts.py 文件，该文件将辅助对 pattern 内容进行解析，以部分简化 aiml 文件的写作。

以文件 "test.aiml" 为例：

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

对于 pattern 中的 fold 标签，将其中的 or 标签内容展开，与原 pattern 文字内容拼接，生成多个 category。

如果使用 unfold_shorts.py 对原 aiml 文件进行解析，需要 **在 `unfdld_list` 中指定目标文件，在 `startup.xml` 文件的 `learn`标签中写入 `-unfold.aiml` 后缀**。

> 注意：pattern 标签中的英文内容需要为全大写

### 2.5 star 用法变更

原 aiml 实现中，通配符 `*` 表示对任意一个单词的匹配。经过修改，现在的 `*` 将匹配 0 或多个单词。

与此对应的，使用 star 标签获取输入的时候，将返回空字符串（没有对应输入）、正确匹配的一个单词、使用空格分割的多个单词（规则匹配的多个输入）。

由于程序中对于普通单词的匹配在对通配符之前，因此可以使用某些技巧。例如以下的 aiml 内容：

```xml
  <category>
    <pattern>什么 是</pattern>
    <template>什么是什么呢？</template>
  </category>
  <category>
    <pattern>* 什么 是 *</pattern>
    <template>我们会为你查询 <star index="2"/></template>
  </category>
```

可以产生对话：

```
user：什么是
bot：什么是什么呢？
user：什么是足球
bot：我们会为你查询 足球
```

