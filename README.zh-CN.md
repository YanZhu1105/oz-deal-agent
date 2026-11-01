# Oz Deal Agent 中文说明

[English](README.md)

Oz Deal Agent 是一个供 Codex 使用的开源技能：从 OzBargain 收集优惠，根据你的兴趣、最低收益和任务周期筛选，再核对商家官网条款。你可以在对话中反馈哪些推荐有用，偏好和反馈保存在本地。

**当前是早期原型。** 选择自动频率后，Agent 会尽可能设置定时采集和 AI 简报，实际能力取决于所用平台和账户；项目本身不提供邮件或 Telegram 托管推送。它与 OzBargain 没有关联。优惠和资格可能变化，请以商家当前条款为准。

## 安装和第一次使用

需要 Git、Python 3.9 以上，以及具备本地技能、文件和网络访问能力的 Codex。Windows 尚未测试；其 Python 环境如果缺少 IANA 时区数据库，可能需要运行 `python -m pip install tzdata`。

```bash
git clone https://github.com/YanZhu1105/oz-deal-agent.git
cd oz-deal-agent
```

在 Codex 中打开这个项目文件夹，然后输入（Claude Code 可使用 `/oz-deal-agent`；尚未完成端到端实测）：

> 使用 `$oz-deal-agent` 设置我的优惠偏好，并查找第一批优惠。

Agent 会展示 17 个板块，并询问五项：关注板块、最低澳元收益、愿意花多久完成条件、是否接受高收益例外，以及简报频率。高收益例外打开后，达到该门槛的优惠可以不受板块和任务周期限制。**任务周期和奖励到账等待时间分开计算。**

首次运行会回查公开的未过期优惠列表并读取新 Deal RSS。回查可能需要几分钟，列表分页和数据来源存在限制，不能保证覆盖全部优惠；候选优惠仍要核对官方网站。你可以在对话中直接反馈推荐是否准确。

## 定时运行

**选择频率后，Agent 应创建并核实定时任务；仅保存偏好不代表定时任务已生效。** 如果你的 Codex 账户支持定时任务，可以要求它按选定时间在当前聊天运行，并确认任务创建成功。电脑需要保持运行；具体功能和额度取决于平台和账户。

RSS 只保留最近一批内容，一天采集一次可能漏帖。可以在终端运行下面的命令，每 15 分钟收集一次，不调用 AI；终端关闭或电脑休眠后即停止：

```bash
python3 .agents/skills/oz-deal-agent/scripts/agent.py watch
```

Windows 若没有 `python3` 命令，可使用 `python`。macOS 也可使用 `python3 .agents/skills/oz-deal-agent/scripts/schedule_collector.py install` 安装每 15 分钟运行的后台采集器；以 `status` 查看服务、以 `uninstall` 停止并保留数据。采集程序本身不会发送简报。

## 数据和使用边界

个人设置、采集记录、反馈和已推送记录保存在 `~/.local/share/oz-deal-agent/`。可以通过 `OZ_DEAL_DATA` 指定目录；同一台机器上的不同用户应使用独立目录。不要把数据库提交到公开仓库，也不要向 Agent 提供银行密码、卡号或身份证件。

反馈会用于后续筛选，不会训练模型。推送去重依赖运行平台确认成功送达；删除数据库会清除推送历史。收益、期限和资格可能变化，所有推荐都应核实奖励和必要费用、领取步骤、适用与排除人群、截止时间和到账条件；信用卡还要检查免息还款、年费和曾持卡限制。申请金融产品前请查看官网最新条款。

开发和测试、完整限制及隐私说明见 [英文 README](README.md)。项目采用 [MIT 许可](LICENSE)。

## 免责与授权

推荐基于网上公开信息，可能不准确或过期；作者和贡献者在适用法律允许的最大范围内不对相关损失承担责任。请自行核实官网条款。完整说明见[免责声明](DISCLAIMER.zh-CN.md)。项目采用 [MIT 许可](LICENSE)。

Grok Bot 用户可参考[实验性适配说明](adapters/grok-bot/README.md)；云端 routine 无法自动读取本机数据库，持久状态与推送去重需要在平台上验证。
