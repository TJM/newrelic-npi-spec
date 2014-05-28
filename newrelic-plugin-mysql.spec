# SPEC FILE for New Relic Platform Installer

# This is a noarch RPM, but the maintainer includes an architechture specific "node" binary, which will be removed.
# These architecture items are used to select the source file only.
%define npi_dir /opt/newrelic-plugins
%define app_dir %{npi_dir}/plugins/com.newrelic.plugins.mysql.instance

Name:           newrelic-plugin-mysql
Version:        2.0.0
Release:        1%{?dist}
Summary:        New Relic MySQL Monitoring Plugin

Group:          Applications/Internet
License:        UNKNOWN
URL:            https://docs.newrelic.com/docs/plugins/installing-an-npi-compatible-plugin


Source0:        https://github.com/newrelic-platform/newrelic_mysql_java_plugin/raw/master/dist/newrelic_mysql_plugin-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXXX)
BuildRequires:  bash 
Requires:       newrelic-platform-installer java-1.7.0

Distribution:   For Internal Use Only
Vendor:         New Relic

%description
New Relic MySQL Monitoring Plugin


%prep
%setup -qn newrelic_mysql_plugin-%{version}


%build
exit 0


%install
mkdir -p %{buildroot}/%{app_dir}
cd ..
tar cf - newrelic_mysql_plugin-%{version} | tar xf - -C %{buildroot}/%{app_dir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{app_dir}
%doc


%post
echo "Successfully setup the New Relic MySQL monitoring plugin!"
echo
echo "Next steps: "
echo "  - Navigate to the directory: '%{npi_dir}'"
echo "  - Run './npi prepare nrmysql' to configure the module"
echo "  - For additional help run the following './npi --help'"

%changelog
