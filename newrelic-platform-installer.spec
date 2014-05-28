# SPEC FILE for New Relic Platform Installer

# This is a noarch RPM, but the maintainer includes an architechture specific "node" binary, which will be removed.
# These architecture items are used to select the source file only.
%define app_platform linux
%define app_arch x64

%define app_dir /opt/newrelic-plugins

Name:           newrelic-platform-installer
Version:        0.1.4
Release:        1%{?dist}
Summary:        New Relic Platform Installer is a command line utility for easily downloading, configuring and running plugins

Group:          Applications/Internet
License:        UNKNOWN
URL:            https://docs.newrelic.com/docs/plugins/installing-an-npi-compatible-plugin


Source0:        https://download.newrelic.com/npi/v%{version}/platform_installer-%{app_platform}-%{app_arch}-v%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXXX)
BuildRequires:  bash nodejs
Requires:       bash nodejs

Distribution:   For Internal Use Only
Vendor:         New Relic

%description
New Relic Platform Installer is a command line utility for easily downloading, configuring and running plugins.


%prep
%setup -qn platform_installer_%{app_platform}_%{app_arch}


%build
echo "Replace arch specific node binary with a symlink to system node"
rm bin/node
ln -s /usr/bin/node bin/node


%install
mkdir -p %{buildroot}/%{app_dir}
tar cf - ./ | tar xf - -C %{buildroot}/%{app_dir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/opt/newrelic-plugins
%doc


%post
/usr/bin/node %{app_dir}/npi.js set distro redhat
/usr/bin/node %{app_dir}/npi.js set user root
echo "Successfully setup the New Relic Platform Installer!"
echo
echo "Next steps: "
echo "  - Navigate to the directory: '$PREFIX'"
echo "  - Run './npi set license_key (paste license key)' to set newrelic license key"
echo "  - Run './npi available' to get a list of available plugins"
echo "  - Run './npi install <plugin>' to download, configure and start a plugin"
echo "  - For additional help run the following './npi --help'"

%changelog
