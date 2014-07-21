# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       maui-settings

# >> macros
# << macros
%define theme maui

Summary:    Customizations for Maui
Version:    0.4.1
Release:    1
Group:      System/Base
License:    MIT
URL:        http://www.maui-project.org/
Source0:    powerdevilrc
Source1:    powerdevilprofilesrc
Source100:  maui-settings.yaml

%description
Customizations for Maui.


%package system
Summary:    Maui default system configuration
Group:      System/Base

%description system
This package configures several aspects of the system to
implement better defaults for Maui.


%package plymouth
Summary:    Maui default configuration for Plymouth
Group:      System/Base
Requires:   plymouth
Requires:   plymouth-plugin-two-step
Requires:   plymouth-theme-%{theme}
Provides:   plymouth-system-theme
Conflicts:  plymouth-system-theme

%description plymouth
This package contains installs and configures the Maui
theme for Plymouth.


%package plasma5
Summary:    Maui default configuration for Plasma 5
Group:      System/Base
Requires:   kde5-filesystem
Requires:   %{theme}-icon-theme
Requires:   %{theme}-cursor-theme
Requires:   %{theme}-plasma-theme
Requires:   %{theme}-wallpapers

%description plasma5
This package implements Maui defaults for Plasma 5.


%prep
# No setup

# >> setup
# << setup

%build
# >> build pre
# << build pre



# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# Create default configuration for Plymouth
mkdir -p %{buildroot}%{_datadir}/plymouth
cat > %{buildroot}%{_datadir}/plymouth/plymouthd.defaults <<EOF
# Distribution defaults. Changes to this file will get overwritten during
# upgrades.
[Daemon]
Theme=%{theme}
EOF

# Avoid Plymouth being interrupted by kernel messages
mkdir -p %{buildroot}%{_libdir}/sysctl.d
cat > %{buildroot}%{_libdir}/sysctl.d/10-console-messages.conf <<EOF
# The following stops low-level messages on console
kernel.printk = 4 5 1 7
EOF

# Configure disk schedulers
mkdir -p %{buildroot}/lib/udev/rules.d
cat > %{buildroot}/lib/udev/rules.d/10-disk-scheduler.rules <<EOF
# Set deadline scheduler for non-rotating disks
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="0", ATTR{queue/scheduler}="deadline"

# Set cfq scheduler for rotating disks
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="1", ATTR{queue/scheduler}="cfq"
EOF

#
# Plasma 5 configuration
#
mkdir -p %{buildroot}%{_sysconfdir}/xdg

# kdeglobals
cat > %{buildroot}%{_sysconfdir}/xdg/kdeglobals <<EOF
[General]
LookAndFeel=org.hawaii.lookandfeel.desktop

[Icons]
Theme=%{theme}
EOF

# kcminput
cat > %{buildroot}%{_sysconfdir}/xdg/kcminputrc <<EOF
[Mouse]
cursorTheme=%{theme}
EOF

# powerdevil
install -D -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/xdg/powerdevilrc
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/powerdevilprofilesrc
# << install pre

# >> install post
# << install post


%files system
%defattr(-,root,root,-)
%{_libdir}/sysctl.d/10-console-messages.conf
/lib/udev/rules.d/10-disk-scheduler.rules
# >> files system
# << files system

%files plymouth
%defattr(-,root,root,-)
%{_datadir}/plymouth/plymouthd.defaults
# >> files plymouth
# << files plymouth

%files plasma5
%defattr(-,root,root,-)
%config %{_sysconfdir}/xdg/kdeglobals
%config %{_sysconfdir}/xdg/kcminputrc
%config %{_sysconfdir}/xdg/powerdevilrc
%config %{_sysconfdir}/xdg/powerdevilprofilesrc
# >> files plasma5
# << files plasma5
