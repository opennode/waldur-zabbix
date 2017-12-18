Name: waldur-zabbix
Summary: Zabbix plugin for Waldur
Group: Development/Libraries
Version: 0.6.0
Release: 1.el7
License: MIT
Url: http://waldur.com
Source0: %{name}-%{version}.tar.gz

Requires: waldur-core >= 0.151.0
Requires: python-zabbix >= 0.7.2

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

%description
Waldur Zabbix adds Zabbix monitoring support to Waldur.

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
* Mon Dec 18 2017 Victor Mireyev <victor@opennodecloud.com> - 0.6.0-1.el7
- Initial version of the package.
