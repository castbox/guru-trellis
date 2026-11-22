# #826 去敏 CLI 验收观察

此附录保留用于复核的事前输入、实际命令和输出。记录按阶段及变体标明原生工具 ID。仅保留与验收有关的事件，个人目录已替换。

## 固定材料

两侧初始项目内容相同，均使用 Codex CLI 0.167.0、deepseek-v4.1-flash 和 high 设置。维护阶段将 add --text 改为 add --message，磁盘 JSON 仍使用 text。

现行方法取自 `f16bb562e4ea844939786cebd5c6c20e686914b2`。候选方法是草稿 `99d49a0fb30833ff588600e5eff3ee0944e9f98e` 与目标 `ffbc25e32e65fa843c0ff0d75a9f16f0e0f0ea8f` 整合后的 Test And Validation Value。运行前固定两份正文。

- 现行正文 SHA-256 `66740871166907dc3619d5766f321cd0b652d76777911e98f99b3872ba6a0fd0`
- 候选正文 SHA-256 `9f6f97852ce536c52b78f9ed5ddec8bfa5ece72ca8d49160335fdb5a04ecc8a3`

### 初始请求

```text
请读取本目录的 method.md 作为本次采用的验证方法。这个小项目需要一份后续维护者可以重复使用的本地验证说明，覆盖通过 CLI 新增并读回一条笔记。先调查项目真实入口，再准备说明并实际验证这条正常路径。把说明和需要留下的观察结果保存在当前项目中。
```

### 维护请求

```text
项目对新增笔记的命令入口做了一个兼容前的调整，请调查实际变更。按本目录 method.md 维护你在本项目已有的验证说明并验证受影响的行为。保留已有、仍有用途的结果。
```

### 评价准则

```text
评价问题：方法是否帮助同一真实 CLI 场景获得可重复、可复核的项目行为证据。
对每侧分别观察：真实入口与可用就绪（已初始化存储且 doctor 可用），实际新增与读回，独立文件副作用，限定清理范围及清理后证据读取，参数变更后的受影响说明与路径重跑、旧证据处理，失败与证据边界。额外观察有独立检出价值的覆盖。评价结论限于本案例。先完成匿名判读，再由 owner 解开映射。
```

### 初始项目入口说明

```markdown
# Local notes
Python 3 standard library only. Run `python3 notes.py --help` for the CLI.
Use your own store path outside project sources. The CLI exposes init, doctor,
add --text, and show. The command help is the source for argument placement.
```

### 初始 CLI 源码

```python
import argparse, json
from pathlib import Path

parser = argparse.ArgumentParser(description="A local notes CLI")
parser.add_argument("--store", type=Path, required=True)
sub = parser.add_subparsers(dest="operation", required=True)
sub.add_parser("init")
sub.add_parser("doctor")
add = sub.add_parser("add")
add.add_argument("--text", required=True)
sub.add_parser("show")
args = parser.parse_args()

if args.operation == "init":
    args.store.parent.mkdir(parents=True, exist_ok=True)
    args.store.write_text("[]", encoding="utf-8")
else:
    rows = json.loads(args.store.read_text(encoding="utf-8"))
    if args.operation == "doctor":
        print(json.dumps({"ready": isinstance(rows, list)}))
    elif args.operation == "add":
        rows.append({"text": args.text})
        args.store.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(rows[-1], ensure_ascii=False))
    elif args.operation == "show":
        print(json.dumps(rows, ensure_ascii=False))
```

## 运行记录

两阶段的四次原生执行退出码均为 0。以下记录保留命令本身、工具退出码和输出。终态只用于证明运行结束。

### A-initial

`item_15`，退出码 `0`。

```text
/bin/zsh -c 'set -eu
RUN_DIR="$(mktemp -d /tmp/local-notes-validation.XXXXXX)"
STORE="$RUN_DIR/notes.json"
NOTE_TEXT='"'local-cli-round-trip-2026-11-22'
printf 'RUN_DIR=%s\\n' \""'$RUN_DIR"
printf '"'STORE=%s\\n' \""'$STORE"
printf '"'Python: '
python3 --version
printf 'Help exit/output:\\n'
python3 notes.py --help | sed -n '1,14p'
printf 'Init:\\n'
python3 notes.py --store \""'$STORE" init
printf '"'Doctor:\\n'
python3 notes.py --store \""'$STORE" doctor
printf '"'Add:\\n'
python3 notes.py --store \""'$STORE" add --text "$NOTE_TEXT"
printf '"'Show:\\n'
python3 notes.py --store \""'$STORE" show
printf '"'Stored bytes:\\n'
wc -c < \""'$STORE"
unlink "$STORE"
rmdir "$RUN_DIR"
printf '"'Cleanup store absent: '
test "'! -e "$STORE"
printf '"'yes\\n'"
RUN_DIR=/tmp/local-notes-validation.iWC8cM
STORE=/tmp/local-notes-validation.iWC8cM/notes.json
Python: Python 3.12.8
Help exit/output:
usage: notes.py [-h] --store STORE {init,doctor,add,show} ...

A local notes CLI

positional arguments:
  {init,doctor,add,show}

options:
  -h, --help            show this help message and exit
  --store STORE
Init:
Doctor:
{"ready": true}
Add:
{"text": "local-cli-round-trip-2026-11-22"}
Show:
[{"text": "local-cli-round-trip-2026-11-22"}]
Stored bytes:
      45
Cleanup store absent: yes
```

`item_20`，退出码 `0`。

```text
/bin/zsh -c "sed -n '1,260p' LOCAL_VALIDATION.md && printf '\\nREADME:\\n' && sed -n '1,120p' README.md"
[产物回读摘录]
# Local CLI validation

This is the repeatable normal-path check for creating a note through the real
CLI and reading it back from the persisted JSON store.

python3 notes.py --store "$STORE" add --text "$NOTE_TEXT"
does not prove the add/read-back journey.
add --text, and show. The command help is the source for argument placement.
```

`item_22`，退出码 `0`。

```text
/bin/zsh -c 'set -eu
RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/local-notes-validation.XXXXXX")"
STORE="$RUN_DIR/notes.json"
NOTE_TEXT='"'local-cli-round-trip-2026-11-22'

cleanup() {
  [ "'! -e "$STORE" ] || unlink "$STORE"
  [ ! -d "$RUN_DIR" ] || rmdir "$RUN_DIR"
}
trap cleanup EXIT

python3 notes.py --store "$STORE" init
python3 notes.py --store "$STORE" doctor
python3 notes.py --store "$STORE" add --text "$NOTE_TEXT"
python3 notes.py --store "$STORE" show

printf '"'store_bytes=%s\\n' \""'$(wc -c < "$STORE")"
cleanup
trap - EXIT
printf '"'store_exists_after_cleanup=%s\\n' \""'$([ -e "$STORE" ] && printf yes || printf no)"'
{"ready": true}
{"text": "local-cli-round-trip-2026-11-22"}
[{"text": "local-cli-round-trip-2026-11-22"}]
store_bytes=      45
store_exists_after_cleanup=no
```

`item_25`，退出码 `0`。

```text
/bin/zsh -c "if find /tmp -maxdepth 1 -type d -name 'local-notes-validation.*' -print -quit | grep -q .; then printf 'validation_dir_remaining\\n'; exit 1; else printf 'no_validation_data_remaining\\n'; fi"
no_validation_data_remaining
```

### A-maintenance

`item_21`，退出码 `1`。

```text
/bin/zsh -c 'RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/local-notes-oldarg.XXXXXX")"; STORE="$RUN_DIR/notes.json"; python3 notes.py --store "$STORE" init; python3 notes.py --store "$STORE" add --text old-argument 2>&1; status=$?; printf '"'exit_status=%s\\n' \""'$status"; [ ! -e "$STORE" ] || unlink "$STORE"; rmdir "$RUN_DIR"; exit 0'
usage: notes.py add [-h] --message MESSAGE
notes.py add: error: the following arguments are required: --message
zsh:1: read-only variable: status
```

`item_26`，退出码 `0`。

```text
/bin/zsh -c "unlink tmp/local-notes-oldarg.kqEnlb/notes.json && rmdir tmp/local-notes-oldarg.kqEnlb && printf 'failed_attempt_cleanup=ok\\n'"
failed_attempt_cleanup=ok
```

`item_28`，退出码 `0`。

```text
/bin/zsh -c 'set -eu
RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/local-notes-validation.XXXXXX")"
STORE="$RUN_DIR/notes.json"
NOTE_MESSAGE='"'local-cli-round-trip-2026-11-22'
cleanup() {
  [ "'! -e "$STORE" ] || unlink "$STORE"
  [ ! -d "$RUN_DIR" ] || rmdir "$RUN_DIR"
}
trap cleanup EXIT
printf '"'run_dir=%s\\n' \""'$RUN_DIR"
python3 notes.py --store "$STORE" init
python3 notes.py --store "$STORE" doctor
python3 notes.py --store "$STORE" add --message "$NOTE_MESSAGE"
python3 notes.py --store "$STORE" show
printf '"'store_bytes=%s\\n' \""'$(wc -c < "$STORE")"
cleanup
trap - EXIT
printf '"'store_exists_after_cleanup=%s\\n' \""'$([ -e "$STORE" ] && printf yes || printf no)"'
run_dir=<project>/tmp/local-notes-validation.TecXIq
{"ready": true}
{"text": "local-cli-round-trip-2026-11-22"}
[{"text": "local-cli-round-trip-2026-11-22"}]
store_bytes=      45
store_exists_after_cleanup=no
```

`item_29`，退出码 `0`。

```text
/bin/zsh -c 'set -u
RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/local-notes-oldarg.XXXXXX")"
STORE="$RUN_DIR/notes.json"
cleanup() {
  [ ! -e "$STORE" ] || unlink "$STORE"
  [ ! -d "$RUN_DIR" ] || rmdir "$RUN_DIR"
}
trap cleanup EXIT
python3 notes.py --store "$STORE" init
printf '"'run_dir=%s\\n' \""'$RUN_DIR"
set +e
OUTPUT="$(python3 notes.py --store "$STORE" add --text old-argument 2>&1)"
rc=$?
set -e
printf '"'%s\\n' \""'$OUTPUT"
printf '"'exit_status=%s\\n' \""'$rc"
cleanup
trap - EXIT'
run_dir=<project>/tmp/local-notes-oldarg.sSZvUE
usage: notes.py add [-h] --message MESSAGE
notes.py add: error: the following arguments are required: --message
exit_status=2
```

`item_34`，退出码 `0`。

```text
/bin/zsh -c "sed -n '1,260p' LOCAL_VALIDATION.md"
[产物回读摘录]
# Local CLI validation

This is the repeatable normal-path check for creating a note through the real
CLI and reading it back from the persisted JSON store.

- The current `add` entry takes the note text through `--message`:
  `python3 notes.py --store PATH add --message TEXT`.
python3 notes.py --store "$STORE" add --message "$NOTE_MESSAGE"
contains the exact message supplied through `add --message`. A successful
`doctor` by itself does not prove the add/read-back journey.
using Python 3.12.8 and the current `add --message` entry.
The current parser does not accept the former `--text` spelling. With an
python3 notes.py --store "$STORE" add --text old-argument
usage: notes.py add [-h] --message MESSAGE
```

`item_35`，退出码 `0`。

```text
/bin/zsh -c "printf '%s\\n' '--- current entry usages ---' && rg -n -- '--message|--text|NOTE_TEXT|NOTE_MESSAGE' README.md notes.py LOCAL_VALIDATION.md && printf '%s\\n' '--- temporary run paths remaining ---' && find tmp -maxdepth 2 \\( -name 'local-notes-validation.*' -o -name 'local-notes-oldarg.*' \\) -print"
[产物回读摘录]
--- current entry usages ---
README.md:4:add --message, and show. The command help is the source for argument placement.
notes.py:10:add.add_argument("--message", required=True)
LOCAL_VALIDATION.md:13:- The current `add` entry takes the note text through `--message`:
LOCAL_VALIDATION.md:14:  `python3 notes.py --store PATH add --message TEXT`.
LOCAL_VALIDATION.md:37:python3 notes.py --store "$STORE" add --message "$NOTE_MESSAGE"
LOCAL_VALIDATION.md:59:contains the exact message supplied through `add --message`. A successful
LOCAL_VALIDATION.md:68:using Python 3.12.8 and the current `add --message` entry.
LOCAL_VALIDATION.md:91:The current parser does not accept the former `--text` spelling. With an
LOCAL_VALIDATION.md:95:python3 notes.py --store "$STORE" add --text old-argument
LOCAL_VALIDATION.md:101:usage: notes.py add [-h] --message MESSAGE
LOCAL_VALIDATION.md:102:notes.py add: error: the following arguments are required: --message
LOCAL_VALIDATION.md:129:`add --text` entry and remains useful as evidence that the then-current
LOCAL_VALIDATION.md:131:verify the current `add --message` parser. The temporary file and directory
```

### B-initial

`item_16`，退出码 `0`。

```text
/bin/zsh -c 'set -eu
temp_dir="$(mktemp -d "${TMPDIR:-/tmp}/local-notes-validation.XXXXXX")"
store="$temp_dir/notes.json"
printf '"'STORE=%s\\n' \""'$store"
python3 notes.py --store "$store" init
python3 notes.py --store "$store" add --text '"'维护验证笔记：CLI 新增并读回'
python3 notes.py --store \""'$store" show
printf '"'PERSISTED_JSON='
cat \""'$store"
printf '"'\\nEXIT=0\\n'"
STORE=<project>/tmp/local-notes-validation.6G0vm2/notes.json
{"text": "维护验证笔记：CLI 新增并读回"}
[{"text": "维护验证笔记：CLI 新增并读回"}]
PERSISTED_JSON=[{"text": "维护验证笔记：CLI 新增并读回"}]
EXIT=0
```

`item_18`，退出码 `0`。

```text
/bin/zsh -c 'set -eu
temp_dir="$(mktemp -d /tmp/local-notes-validation.XXXXXX)"
store="$temp_dir/notes.json"
printf '"'STORE=%s\\n' \""'$store"
python3 notes.py --store "$store" init
python3 notes.py --store "$store" add --text '"'维护验证笔记：CLI 新增并读回'
python3 notes.py --store \""'$store" show
printf '"'PERSISTED_JSON='
cat \""'$store"
printf '"'\\nEXIT=0\\n'"
STORE=/tmp/local-notes-validation.wdvAxN/notes.json
{"text": "维护验证笔记：CLI 新增并读回"}
[{"text": "维护验证笔记：CLI 新增并读回"}]
PERSISTED_JSON=[{"text": "维护验证笔记：CLI 新增并读回"}]
EXIT=0
```

`item_22`，退出码 `0`。

```text
/bin/zsh -c 'python3 notes.py --store /tmp/local-notes-validation.wdvAxN/notes.json doctor'
{"ready": true}
```

`item_28`，退出码 `0`。

```text
/bin/zsh -c "sed -n '1,280p' LOCAL_VALIDATION.md"
[产物回读摘录]
# 本地验证说明：CLI 新增并读回笔记

## 验证目标

从项目真实 CLI 入口初始化一个独立笔记存储，新增一条笔记，再由新的
- `add` 子命令还需要紧随其后的 `--text` 参数。
python3 notes.py --store "$store" add --text "$note"
$ python3 notes.py --store /tmp/local-notes-validation.wdvAxN/notes.json add --text '维护验证笔记：CLI 新增并读回'
```

`item_31`，退出码 `0`。

```text
/bin/zsh -c 'set -eu
unlink /tmp/local-notes-validation.wdvAxN/notes.json
rmdir /tmp/local-notes-validation.wdvAxN
unlink tmp/local-notes-validation.6G0vm2/notes.json
rmdir tmp/local-notes-validation.6G0vm2
find tmp -maxdepth 2 -print'
tmp
tmp/.tmpWS3265
tmp/.tmphzilnP
```

### B-maintenance

`item_20`，退出码 `0`。

```text
/bin/zsh -c 'validation_dir="$(mktemp -d /tmp/local-notes-old-flag.XXXXXX)"
store="$validation_dir/notes.json"
printf '"'VALIDATION_DIR=%s\\n' \""'$validation_dir"
python3 notes.py --store "$store" init
old_output=$(python3 notes.py --store "$store" add --text '"'旧参数诊断' 2>&1)
old_exit="'$?
printf '"'OLD_FLAG_EXIT=%s\\n' \""'$old_exit"
printf '"'%s\\n' \""'$old_output"
printf '"'STORE_AFTER_REJECTION='
cat \""'$store"
printf '"'\\n'"
VALIDATION_DIR=/tmp/local-notes-old-flag.7dVF01
OLD_FLAG_EXIT=2
usage: notes.py add [-h] --message MESSAGE
notes.py add: error: the following arguments are required: --message
STORE_AFTER_REJECTION=[]
```

`item_21`，退出码 `0`。

```text
/bin/zsh -c 'set -e
validation_dir="$(mktemp -d /tmp/local-notes-validation.XXXXXX)"
store="$validation_dir/notes.json"
note='"'维护验证笔记：CLI 新增并读回'
printf 'VALIDATION_DIR=%s\\n' \""'$validation_dir"
python3 notes.py --store "$store" init
printf '"'INIT_EXIT=%s\\n' \""'$?"
python3 notes.py --store "$store" add --message "$note"
printf '"'ADD_EXIT=%s\\n' \""'$?"
python3 notes.py --store "$store" show
printf '"'SHOW_EXIT=%s\\n' \""'$?"
printf '"'PERSISTED_JSON='
cat \""'$store"
printf '"'\\n'
python3 --version"
VALIDATION_DIR=/tmp/local-notes-validation.2xFDIT
INIT_EXIT=0
{"text": "维护验证笔记：CLI 新增并读回"}
ADD_EXIT=0
[{"text": "维护验证笔记：CLI 新增并读回"}]
SHOW_EXIT=0
PERSISTED_JSON=[{"text": "维护验证笔记：CLI 新增并读回"}]
Python 3.12.8
```

`item_31`，退出码 `0`。

```text
/bin/zsh -c "sed -n '1,220p' LOCAL_VALIDATION.md"
[产物回读摘录]
# 本地验证说明：CLI 新增并读回笔记

## 验证目标

从项目真实 CLI 入口初始化一个独立笔记存储，新增一条笔记，再由新的
- `add` 通过当前声明的 `--message` 参数接收笔记正文。
本目录没有 Git 元数据，因此不能从提交历史确认变更原因。按当前命令帮助、入口
- 旧验证记录的调用方式为 `add --text`。
- 当前 `python3 notes.py add --help` 只声明 `--message MESSAGE`。
- 当前入口实现也只注册了 `--message`，没有保留 `--text` 别名。
- `add` 子命令通过 `--message` 接收笔记正文。
python3 notes.py --store "$store" add --message "$note"
$ python3 notes.py --store /tmp/local-notes-validation.2xFDIT/notes.json add --message '维护验证笔记：CLI 新增并读回'
$ python3 notes.py --store /tmp/local-notes-old-flag.7dVF01/notes.json add --text '旧参数诊断'
```

`item_32`，退出码 `0`。

```text
/bin/zsh -c "rg -n -- '--text|--message|2xFDIT|wdvAxN|7dVF01|退出码' LOCAL_VALIDATION.md"
[产物回读摘录]
8:- `init`、`add`、`show` 均以退出码 `0` 完成。
9:- `add` 通过当前声明的 `--message` 参数接收笔记正文。
22:- 旧验证记录的调用方式为 `add --text`。
23:- 当前 `python3 notes.py add --help` 只声明 `--message MESSAGE`。
24:- 当前入口实现也只注册了 `--message`，没有保留 `--text` 别名。
36:- `add` 子命令通过 `--message` 接收笔记正文。
53:python3 notes.py --store "$store" add --message "$note"
92:$ python3 notes.py --store /tmp/local-notes-validation.2xFDIT/notes.json add --message '维护验证笔记：CLI 新增并读回'
112:$ python3 notes.py --store /tmp/local-notes-old-flag.7dVF01/notes.json add --text '旧参数诊断'
113:usage: notes.py add [-h] --message MESSAGE
114:notes.py add: error: the following arguments are required: --message
121:这说明当前版本不接受 `--text`，且参数解析失败发生在写入之前，存储仍为空。证据
126:以下结果产生于入口参数仍为 `--text` 的旧版本，保留作为同一正常路径的历史基线：
129:$ python3 notes.py --store /tmp/local-notes-validation.wdvAxN/notes.json add --text '维护验证笔记：CLI 新增并读回'
```

`item_39`，退出码 `0`。

```text
/bin/zsh -c "unlink __pycache__/notes.cpython-312.pyc
rmdir __pycache__
unlink /tmp/local-notes-validation.2xFDIT/notes.json
rmdir /tmp/local-notes-validation.2xFDIT
unlink /tmp/local-notes-old-flag.7dVF01/notes.json
rmdir /tmp/local-notes-old-flag.7dVF01
printf 'CLEANUP_OK\\n'"
CLEANUP_OK
```

## 评价与解盲

评价完成后读取映射。A 为候选，B 为现行。

以下为匿名评价的结论摘录。各侧逐项依据见上面的工具记录。

## 对照结论

两侧都覆盖了真实 CLI 的核心闭环，都正确识别并重跑了参数变更后的 `--message` 路径，也都把旧 `--text` 结果降级为历史证据。两侧都不是仅凭 `doctor` 或源码静态读取下结论。

A 的优势是维护阶段同时覆盖了 `doctor`，且清理后有明确的存在性读取。A 的主要不足是当前实测数据落入项目 `tmp`，与其“项目外临时存储”的口径不完全一致；旧参数拒绝后也没有直接证明 store 未被写入，最终说明缺少独立证据边界章节。

B 的优势是当前路径固定在 `/tmp`、直接核对了持久化内容、明确证明旧参数失败后 store 仍为空，并在最终产物中完整呈现变更影响、历史证据失效边界和未覆盖范围。B 的主要不足是维护阶段未再次运行 `doctor`，清理后缺少一次独立的存在性复查。

就本案例的评价问题而言，B 的维护阶段证据链更完整、更可直接复核；A 也获得了可用的行为证据，但项目内临时副作用和较弱失败边界使其可重复性与可复核性略逊。未使用任何变体身份信息；最终结论仅限本案例。
