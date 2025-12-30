# diskimage-builder 與 Oz 的差異比較

## 簡介

本文檔比較 OpenStack 的 diskimage-builder 和 Clalancette 的 Oz 兩種映像構建工具的差異。

## 主要差異

### 1. diskimage-builder (DIB)

**官方網站**: https://docs.openstack.org/diskimage-builder/latest/

**特點**:
- OpenStack 項目的一部分
- 使用 **chroot** 環境來構建映像，**不需要啟動完整的 VM**
- 基於元素(elements)的模塊化設計
- 支援多種 Linux 發行版 (Ubuntu, CentOS, Fedora, Debian 等)
- 可以產生多種格式的映像 (qcow2, raw, vhd, vmdk 等)

**工作原理**:
1. 創建一個基礎的文件系統
2. 在 chroot 環境中安裝軟件包和配置系統
3. 應用自定義腳本和配置
4. 生成最終映像

**Kickstart 支援**:
- **不直接使用** kickstart 文件
- 使用 element 系統來定義映像構建邏輯
- 可以通過自定義 element 腳本實現類似 kickstart 的功能

### 2. Oz

**官方網站**: https://github.com/clalancette/oz

**特點**:
- 獨立的映像構建工具
- **使用 KVM 啟動完整的虛擬機**來安裝和配置系統
- 基於模板定義 (TDL - Template Description Language)
- 主要針對 RHEL、CentOS、Fedora 等紅帽系發行版

**工作原理**:
1. 使用 libvirt/KVM 創建虛擬機
2. 在虛擬機中執行完整的操作系統安裝過程
3. 使用 anaconda 安裝程序和 kickstart 文件
4. 安裝完成後，客製化虛擬機
5. 關閉虛擬機並保存映像

**Kickstart 支援**:
- **完全支援** kickstart 文件
- 可以直接使用標準的 anaconda kickstart 配置
- 支援所有 kickstart 指令和選項

## 詳細比較表

| 特性 | diskimage-builder | Oz |
|------|-------------------|-----|
| 構建方式 | chroot 環境 | KVM 虛擬機 |
| 需要虛擬化 | 否 | 是 (需要 KVM) |
| Kickstart 支援 | 不直接支援 | 完全支援 |
| 構建速度 | 較快 | 較慢 (需要啟動 VM) |
| 資源消耗 | 較低 | 較高 (需要 VM 資源) |
| 適用發行版 | 多種 Linux 發行版 | 主要是紅帽系 |
| 配置方式 | Element 腳本 | TDL + Kickstart |
| 社群支援 | OpenStack 社群 | 獨立項目 |
| 主要用途 | OpenStack 雲映像 | 通用 VM 映像 |

## KVM 使用說明

### diskimage-builder:
- **不使用 KVM** 啟動虛擬機
- 使用 chroot 在主機上直接構建映像
- 更輕量級，但可能需要處理一些 chroot 環境的限制

### Oz:
- **使用 KVM** 啟動完整的虛擬機
- 在真實的虛擬化環境中安裝操作系統
- 更接近真實的安裝過程，但需要更多資源

## Kickstart 文件編輯

### diskimage-builder:
```bash
# diskimage-builder 不直接使用 kickstart
# 需要創建自定義 element
# 範例：在 element 中執行配置腳本

mkdir -p my-element/install.d
cat > my-element/install.d/99-custom-config <<EOF
#!/bin/bash
# 您的自定義配置
yum install -y httpd
systemctl enable httpd
EOF
chmod +x my-element/install.d/99-custom-config

# 構建映像
disk-image-create -o my-image centos-minimal my-element
```

### Oz:
```bash
# Oz 可以直接使用 kickstart 文件
# 1. 創建 kickstart 文件
cat > my-kickstart.ks <<EOF
install
text
lang en_US.UTF-8
keyboard us
network --bootproto=dhcp
rootpw --plaintext password
timezone UTC
bootloader --location=mbr
zerombr
clearpart --all --initlabel
autopart

%packages
@core
httpd
%end

%post
systemctl enable httpd
%end
EOF

# 2. 創建 TDL 模板
cat > centos.tdl <<EOF
<template>
  <name>centos7</name>
  <os>
    <name>CentOS-7</name>
    <version>7</version>
    <arch>x86_64</arch>
    <install type='url'>
      <url>http://mirror.centos.org/centos/7/os/x86_64/</url>
    </install>
  </os>
  <description>CentOS 7 Template</description>
</template>
EOF

# 3. 使用 Oz 構建映像
oz-install -d3 -u my-kickstart.ks centos.tdl
```

## 選擇建議

### 使用 diskimage-builder 的情況:
- 需要為 OpenStack 構建雲映像
- 不想啟動完整的虛擬機
- 需要快速構建映像
- 需要支援多種 Linux 發行版

### 使用 Oz 的情況:
- 已經有現成的 kickstart 文件
- 需要完全按照標準安裝流程構建映像
- 主要使用紅帽系發行版
- 需要完整的 anaconda 安裝功能

## 實際使用案例

### 案例：建立客製化 Rocky Linux 9 實體機安裝映像

**需求場景**:
- 目標：建立客製化的 Rocky Linux 9 映像
- 用途：安裝在實體機硬碟上
- 客製化內容：
  - RPM 套件安裝
  - 客製化檔案預先放置在映像中
- 環境限制：只能連線到自建的 RPM 鏡像站和檔案伺服器

**建議工具：Oz**

**推薦理由**:

1. **完整的 Kickstart 支援**
   - 可以在 kickstart 文件中指定自建的 RPM 鏡像站
   - 支援所有 anaconda 安裝選項，與實體機安裝流程一致

2. **自訂 RPM 來源**
   ```bash
   # 在 kickstart 文件中設定自建鏡像站
   url --url=http://your-mirror-server.local/rocky/9/BaseOS/x86_64/os/
   repo --name="AppStream" --baseurl=http://your-mirror-server.local/rocky/9/AppStream/x86_64/os/
   repo --name="custom" --baseurl=http://your-mirror-server.local/custom-rpms/
   ```

3. **預先放置客製化檔案**
   ```bash
   # 在 kickstart 的 %post 段落中
   %post
   # 從檔案伺服器下載客製化檔案
   curl http://your-file-server.local/custom-configs/app.conf -o /etc/app.conf
   curl http://your-file-server.local/scripts/init-script.sh -o /usr/local/bin/init-script.sh
   chmod +x /usr/local/bin/init-script.sh
   
   # 或直接在 kickstart 中內嵌檔案內容
   cat > /etc/custom-config.conf <<EOF
   # 您的客製化配置
   EOF
   %end
   ```

4. **適合實體機部署**
   - Oz 產生的映像與標準 anaconda 安裝流程完全相同
   - 可以直接用於實體機安裝，無需額外調整

**完整範例**:

```bash
# 1. 建立 kickstart 文件（my-rocky9.ks）
cat > my-rocky9.ks <<'EOF'
install
text
lang en_US.UTF-8
keyboard us
network --bootproto=dhcp --hostname=rocky9-custom

# 使用自建鏡像站
url --url=http://your-mirror-server.local/rocky/9/BaseOS/x86_64/os/
repo --name="AppStream" --baseurl=http://your-mirror-server.local/rocky/9/AppStream/x86_64/os/
repo --name="custom" --baseurl=http://your-mirror-server.local/custom-rpms/

rootpw --plaintext yourpassword
timezone Asia/Taipei

bootloader --location=mbr
zerombr
clearpart --all --initlabel
autopart

# 安裝客製化套件
%packages
@core
@standard
httpd
nginx
custom-package-1
custom-package-2
%end

# 客製化配置
%post --log=/root/ks-post.log
# 從檔案伺服器下載客製化檔案
curl -o /etc/app.conf http://your-file-server.local/configs/app.conf
curl -o /usr/local/bin/setup.sh http://your-file-server.local/scripts/setup.sh
chmod +x /usr/local/bin/setup.sh

# 執行客製化設定
systemctl enable httpd
systemctl enable nginx

# 建立客製化使用者
useradd -m -s /bin/bash customuser
%end
EOF

# 2. 建立 TDL 模板（rocky9.tdl）
cat > rocky9.tdl <<'EOF'
<template>
  <name>rocky9-custom</name>
  <os>
    <name>Rocky-9</name>
    <version>9</version>
    <arch>x86_64</arch>
    <install type='url'>
      <url>http://your-mirror-server.local/rocky/9/BaseOS/x86_64/os/</url>
    </install>
  </os>
  <description>Rocky Linux 9 Custom Image for Physical Deployment</description>
</template>
EOF

# 3. 使用 Oz 建立映像
oz-install -d3 -u my-rocky9.ks rocky9.tdl

# 4. 生成的映像可用於：
# - 直接寫入 USB 安裝碟
# - 透過 PXE 網路安裝
# - 作為 ISO 映像刻錄光碟
```

**為什麼不選擇 diskimage-builder？**

diskimage-builder 在此場景下的限制：
1. 不直接支援 kickstart，需要重寫所有配置邏輯為 element 腳本
2. 需要學習 element 系統，增加學習成本
3. 如果已經有 kickstart 經驗，無法直接重用知識
4. 對於實體機安裝，Oz 的標準安裝流程更可靠

## 總結

**主要差異回答**:
1. **構建方式**: diskimage-builder 使用 chroot 環境，Oz 使用 KVM 虛擬機
2. **KVM 使用**: diskimage-builder **不使用** KVM，Oz **使用** KVM 啟動 VM 後修改 image
3. **Kickstart 支援**: diskimage-builder **不直接支援** kickstart，Oz **完全支援**且可以自行編輯 kickstart 檔案

---

# Comparison: diskimage-builder vs Oz

## Introduction

This document compares two image building tools: OpenStack's diskimage-builder and Clalancette's Oz.

## Key Differences

### 1. diskimage-builder (DIB)

**Official Website**: https://docs.openstack.org/diskimage-builder/latest/

**Features**:
- Part of the OpenStack project
- Uses **chroot** environment to build images, **does not require starting a full VM**
- Modular design based on elements
- Supports multiple Linux distributions (Ubuntu, CentOS, Fedora, Debian, etc.)
- Can produce images in various formats (qcow2, raw, vhd, vmdk, etc.)

**How it works**:
1. Creates a base filesystem
2. Installs packages and configures the system in a chroot environment
3. Applies custom scripts and configurations
4. Generates the final image

**Kickstart Support**:
- **Does not directly use** kickstart files
- Uses element system to define image building logic
- Can achieve kickstart-like functionality through custom element scripts

### 2. Oz

**Official Website**: https://github.com/clalancette/oz

**Features**:
- Independent image building tool
- **Uses KVM to start a full virtual machine** for system installation and configuration
- Based on Template Description Language (TDL)
- Primarily targets RHEL, CentOS, Fedora, and other Red Hat-based distributions

**How it works**:
1. Creates a virtual machine using libvirt/KVM
2. Performs a complete operating system installation in the VM
3. Uses anaconda installer with kickstart files
4. Customizes the VM after installation
5. Shuts down the VM and saves the image

**Kickstart Support**:
- **Fully supports** kickstart files
- Can directly use standard anaconda kickstart configurations
- Supports all kickstart directives and options

## Detailed Comparison Table

| Feature | diskimage-builder | Oz |
|---------|-------------------|-----|
| Build Method | chroot environment | KVM virtual machine |
| Requires Virtualization | No | Yes (requires KVM) |
| Kickstart Support | Not directly supported | Fully supported |
| Build Speed | Faster | Slower (needs to start VM) |
| Resource Usage | Lower | Higher (requires VM resources) |
| Supported Distributions | Multiple Linux distributions | Primarily Red Hat-based |
| Configuration Method | Element scripts | TDL + Kickstart |
| Community Support | OpenStack community | Independent project |
| Primary Use Case | OpenStack cloud images | General VM images |

## KVM Usage

### diskimage-builder:
- **Does not use KVM** to start virtual machines
- Uses chroot to build images directly on the host
- More lightweight, but may need to handle some chroot environment limitations

### Oz:
- **Uses KVM** to start a full virtual machine
- Installs the operating system in a real virtualized environment
- Closer to the actual installation process, but requires more resources

## Editing Kickstart Files

### diskimage-builder:
```bash
# diskimage-builder does not directly use kickstart
# Need to create custom elements
# Example: Execute configuration scripts in elements

mkdir -p my-element/install.d
cat > my-element/install.d/99-custom-config <<EOF
#!/bin/bash
# Your custom configuration
yum install -y httpd
systemctl enable httpd
EOF
chmod +x my-element/install.d/99-custom-config

# Build image
disk-image-create -o my-image centos-minimal my-element
```

### Oz:
```bash
# Oz can directly use kickstart files
# 1. Create kickstart file
cat > my-kickstart.ks <<EOF
install
text
lang en_US.UTF-8
keyboard us
network --bootproto=dhcp
rootpw --plaintext password
timezone UTC
bootloader --location=mbr
zerombr
clearpart --all --initlabel
autopart

%packages
@core
httpd
%end

%post
systemctl enable httpd
%end
EOF

# 2. Create TDL template
cat > centos.tdl <<EOF
<template>
  <name>centos7</name>
  <os>
    <name>CentOS-7</name>
    <version>7</version>
    <arch>x86_64</arch>
    <install type='url'>
      <url>http://mirror.centos.org/centos/7/os/x86_64/</url>
    </install>
  </os>
  <description>CentOS 7 Template</description>
</template>
EOF

# 3. Build image using Oz
oz-install -d3 -u my-kickstart.ks centos.tdl
```

## Recommendations

### Use diskimage-builder when:
- Building cloud images for OpenStack
- Don't want to start a full virtual machine
- Need to build images quickly
- Need to support multiple Linux distributions

### Use Oz when:
- Already have existing kickstart files
- Need to build images following standard installation procedures
- Primarily using Red Hat-based distributions
- Need full anaconda installation functionality

## Real-World Use Case

### Use Case: Building a Custom Rocky Linux 9 Image for Physical Machine Deployment

**Scenario Requirements**:
- Goal: Create a customized Rocky Linux 9 image
- Purpose: Installation on physical machine hard drives
- Customization needs:
  - RPM package installation
  - Pre-configured custom files included in the image
- Environment constraints: Can only connect to self-hosted RPM mirror and file server

**Recommended Tool: Oz**

**Reasons for Recommendation**:

1. **Full Kickstart Support**
   - Can specify custom RPM mirror in kickstart file
   - Supports all anaconda installation options, consistent with physical installation process

2. **Custom RPM Sources**
   ```bash
   # Configure custom mirror in kickstart file
   url --url=http://your-mirror-server.local/rocky/9/BaseOS/x86_64/os/
   repo --name="AppStream" --baseurl=http://your-mirror-server.local/rocky/9/AppStream/x86_64/os/
   repo --name="custom" --baseurl=http://your-mirror-server.local/custom-rpms/
   ```

3. **Pre-placing Custom Files**
   ```bash
   # In kickstart %post section
   %post
   # Download custom files from file server
   curl http://your-file-server.local/custom-configs/app.conf -o /etc/app.conf
   curl http://your-file-server.local/scripts/init-script.sh -o /usr/local/bin/init-script.sh
   chmod +x /usr/local/bin/init-script.sh
   
   # Or embed file content directly in kickstart
   cat > /etc/custom-config.conf <<EOF
   # Your custom configuration
   EOF
   %end
   ```

4. **Suitable for Physical Deployment**
   - Images produced by Oz are identical to standard anaconda installation
   - Can be used directly for physical machine installation without additional adjustments

**Complete Example**:

```bash
# 1. Create kickstart file (my-rocky9.ks)
cat > my-rocky9.ks <<'EOF'
install
text
lang en_US.UTF-8
keyboard us
network --bootproto=dhcp --hostname=rocky9-custom

# Use custom mirror
url --url=http://your-mirror-server.local/rocky/9/BaseOS/x86_64/os/
repo --name="AppStream" --baseurl=http://your-mirror-server.local/rocky/9/AppStream/x86_64/os/
repo --name="custom" --baseurl=http://your-mirror-server.local/custom-rpms/

rootpw --plaintext yourpassword
timezone Asia/Taipei

bootloader --location=mbr
zerombr
clearpart --all --initlabel
autopart

# Install custom packages
%packages
@core
@standard
httpd
nginx
custom-package-1
custom-package-2
%end

# Custom configuration
%post --log=/root/ks-post.log
# Download custom files from file server
curl -o /etc/app.conf http://your-file-server.local/configs/app.conf
curl -o /usr/local/bin/setup.sh http://your-file-server.local/scripts/setup.sh
chmod +x /usr/local/bin/setup.sh

# Execute custom setup
systemctl enable httpd
systemctl enable nginx

# Create custom user
useradd -m -s /bin/bash customuser
%end
EOF

# 2. Create TDL template (rocky9.tdl)
cat > rocky9.tdl <<'EOF'
<template>
  <name>rocky9-custom</name>
  <os>
    <name>Rocky-9</name>
    <version>9</version>
    <arch>x86_64</arch>
    <install type='url'>
      <url>http://your-mirror-server.local/rocky/9/BaseOS/x86_64/os/</url>
    </install>
  </os>
  <description>Rocky Linux 9 Custom Image for Physical Deployment</description>
</template>
EOF

# 3. Build image using Oz
oz-install -d3 -u my-rocky9.ks rocky9.tdl

# 4. The generated image can be used for:
# - Directly writing to USB installation media
# - PXE network installation
# - Burning to ISO for CD/DVD
```

**Why Not diskimage-builder?**

Limitations of diskimage-builder for this scenario:
1. Does not directly support kickstart; requires rewriting all configuration logic as element scripts
2. Requires learning the element system, increasing learning curve
3. Cannot reuse existing kickstart knowledge and experience
4. For physical machine installation, Oz's standard installation process is more reliable

## Summary

**Answers to the Main Questions**:
1. **Build Method**: diskimage-builder uses chroot environment, Oz uses KVM virtual machines
2. **KVM Usage**: diskimage-builder **does not use** KVM, Oz **uses** KVM to start VMs and then modify images
3. **Kickstart Support**: diskimage-builder **does not directly support** kickstart, Oz **fully supports** it and allows editing kickstart files

## References

- [diskimage-builder Documentation](https://docs.openstack.org/diskimage-builder/latest/)
- [Oz GitHub Repository](https://github.com/clalancette/oz)
- [Oz Wiki](https://github.com/clalancette/oz/wiki)
- [Kickstart Documentation](https://pykickstart.readthedocs.io/)
