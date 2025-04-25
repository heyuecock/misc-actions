glados家备用机场的自动签到脚本。
需要gmail邮箱账号，不是gmail的话可以自己稍微调试一下。
用的浏览器模拟技术，比较稳定，邮件监听而不是轮询。手搓代码，质量还行。
一天两次防止意外签到失败，一次1分钟，一个月需要消耗大概60分钟actions用量。
最好是不要fork而是clone获取源代码，自己的账号稳定用了1个月，会员天数涨了20天。

以下是AI生成：

🎉 GLaDOS 机场自动签到脚本，告别每日烦恼！ 🎉

各位GLaDOS用户，是否厌倦了每天手动签到？ 现在，通过我的脚本，你可以完全自动化这个过程，享受更轻松的网络体验！

核心特性：

稳定可靠： 使用Playwright模拟真实浏览器行为，非Cookie登录，告别Cookie失效问题，一个月稳定运行有保障！
完全自动化： 无需人工干预，每天自动签到，解放双手。
GitHub Actions： 利用GitHub Actions实现定时任务，无需服务器。
使用方法（新手友好）：

GitHub 仓库： 先 Star 我开源仓库: https://github.com/lhoeger5/misc-actions

克隆或 Fork： 将仓库克隆到本地，或 Fork 到你的 GitHub 账户。

重要！重命名文件夹： 将仓库中的 github 文件夹 重命名 为 .github 文件夹！

设置 Secrets： 在你的 GitHub 仓库中，进入 "Settings" -> "Secrets and variables" -> "Actions"，创建两个新的 Secrets：

GLADOS_EMAIL: 你的GLaDOS账户对应的 Gmail 邮箱地址。
GLADOS_PASSWORD: 你的Gmail的 应用专用密码 （务必使用应用专用密码，不要直接使用你的 Gmail 密码！）。
如何创建 Gmail 应用专用密码：

访问你的 Google 账户：https://myaccount.google.com/
在左侧导航栏中，点击“安全性”。
在“您登录 Google 的方式”部分，开启“两步验证”（如果尚未开启）。
开启两步验证后，返回“安全性”页面，在“您可以使用的方式验证身份”部分，找到“应用专用密码”。
点击“应用专用密码”，然后选择“应用”为“其他（自定义名称）”，并输入一个名称（例如：GLaDOS）。
点击“生成”，然后复制生成的 16 位应用专用密码。
邮箱支持： 目前脚本 仅支持 Gmail！ 如果你使用的是其他邮箱，需要自行修改 glados/main.py 文件第33行关于 IMAP 服务器地址的部分。

启用 Actions： 确保你的仓库启用了 Actions。

手动触发（可选）： 为了测试，可以在 "Actions" 中手动运行 "GLADOS 自动签到" 工作流，看看是否一切正常。

为什么选择这个脚本？

市面上有很多 GLaDOS 自动签到脚本，但大多数基于 Cookie 登录，容易失效。我的脚本使用 Playwright 模拟浏览器，更加稳定可靠，能有效避免因 Cookie 失效导致的签到失败问题。已经稳定运行一个月了，欢迎大家来测试！

注意事项：

务必使用 Gmail 应用专用密码！
务必将 github 文件夹重命名为 .github 文件夹！
如果使用非 Gmail 邮箱，需要自行修改代码。
首次运行可能需要安装 Playwright 浏览器，请耐心等待。
欢迎各位体验，如有问题，欢迎在 GitHub 仓库中提交 issue！
