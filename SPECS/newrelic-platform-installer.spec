# SPEC FILE for NewRelic Platform Installer

# This RPM is re-package of the NewRelic Platform Installer, which includes
# an architechture specific "node" binary, which will be removed for EL6.
# These architecture items are used to select the source file.

# They use "nodejs" style architecture
%ifarch x86_64
%define app_arch x64
%endif

%ifarch i386 i486 i586 i686
%define app_arch x86
%endif

%define app_platform linux
%define app_dir /opt/newrelic-plugins

Name:           newrelic-platform-installer
Version:        0.1.5
Release:        1%{?dist}
Summary:        New Relic Platform Installer

Group:          Applications/Internet
License:        UNKNOWN
URL:            https://docs.newrelic.com/docs/plugins/installing-an-npi-compatible-plugin


Source0:        https://download.newrelic.com/npi/v%{version}/platform_installer-%{app_platform}-%{app_arch}-v%{version}.tar.gz

# RHEL / CentOS 6 can be noarch (see build section too)
# Could probably add a Fedora Core number too, but I don't know which one
%if 0%{rhel} >= 6
BuildArch:      noarch
Requires:       nodejs
%else
#Requires:       bash
%endif

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXXX)
BuildRequires:  bash

Distribution:   For Internal Use Only
Vendor:         New Relic

%description
New Relic Platform Installer is a command line utility for easily downloading, configuring and running plugins.


%prep
%setup -qn platform_installer_%{app_platform}_%{app_arch}


%build
# RHEL / CentOS 6 remove included node binary to make it noarch
# Could probably add a Fedora Core number too, but I don't know which one
%if 0%{rhel} >= 6
  echo "Replace arch specific node binary with a symlink to system node"
  rm bin/node
  ln -s /usr/bin/node bin/node
%endif
exit 0


%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{app_dir}
%{__cp} -r ./ %{buildroot}/%{app_dir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{app_dir}
%doc


%post
# Apply initial configuration
if [ ! -f %{app_dir}/config/newrelic.js ]; then
  /usr/bin/node %{app_dir}/npi.js set distro redhat
  /usr/bin/node %{app_dir}/npi.js set user root
fi
  echo "Successfully setup the New Relic Platform Installer!"
  echo
  echo "Next steps: "
  echo "  - Navigate to the directory: '${app_dir}'"
  echo "  - Run './npi set license_key (paste license key)' to set newrelic license key"
  echo "  - Run './npi available' to get a list of available plugins"
  echo "  - Run './npi install <plugin>' to download, configure and start a plugin"
  echo "  - For additional help run the following './npi --help'"
  echo " or https://docs.newrelic.com/docs/plugins/installing-an-npi-compatible-plugin"


%changelog
* Fri May 30 2014 Tommy McNeely <tmcneely@deliveryagent.com> - 0.1.5-1
- Update to v0.1.5
- Fix Issue #1 - post script was overriding existing config
- Update spec to work with EL5 (and architectures)


* Wed May 28 2014 Tommy McNeely <tmcneely@deliveryagent.com> - 0.1.4-3
- Added a fix for working with proxies - https://discuss.newrelic.com/t/proxy-settings-do-not-appear-to-be-working/1873/7

