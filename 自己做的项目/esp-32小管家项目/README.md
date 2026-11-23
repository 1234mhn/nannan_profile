# ESP-32 小管家项目

## 项目目标

制作一个属于自己的实体小管家：

- 通过 ESP32-S3 接收语音
- 连接腾讯云服务器上的 OpenClaw
- 记录每天的文字、音频、图片和视频
- 通过多个 Agent 自动整理、分类和总结
- 后续支持控制本地 Mac 电脑
- 危险操作通过实体按钮确认

## 总体架构

```text
你喊“小管家”
      ↓
ESP32-S3 语音终端
      ↓ Wi-Fi
腾讯云 Ubuntu 24.04 云服务器
      ↓
OpenClaw 总控 Agent
      ├─ 记录 Agent
      ├─ 整理 Agent
      ├─ 搜索 Agent
      ├─ 总结 Agent
      └─ Mac 执行 Agent
      ↓
数据库 / 文件存储 / 知识库
```

## 当前状态

- [x] 腾讯云服务器已部署 OpenClaw
- [x] 微信接口已连接 OpenClaw
- [x] 已确认服务器系统为 Ubuntu 24.04 LTS
- [x] 已确认 OpenClaw 不是 Docker 部署
- [x] 已确认 OpenClaw 命令路径为 `/root/.local/share/pnpm/openclaw`
- [ ] 为 OpenClaw 配置安全 API/Webhook 入口
- [ ] 测试 ESP32-S3 开发板
- [ ] 实现 ESP32 录音上传
- [ ] 实现 OpenClaw 语音记录
- [ ] 接入图片和视频记录
- [ ] 接入本地 Mac 执行器

## 安全原则

- 不把 OpenClaw 管理端口直接暴露到公网
- API 使用独立 Token
- 删除文件、执行命令、发送消息等操作需要人工确认
- 文档中不保存密码、API Key、Token 和完整公网 IP
