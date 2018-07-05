Name: waldur-zabbix
Summary: Zabbix plugin for Waldur
Group: Development/Libraries
Version: 0.8.4
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
* Thu Jul 5 2018 Jenkins <jenkins@opennodecloud.com> - 0.8.4-1.el7
- New upstream release

* Sun Jun 24 2018 Jenkins <jenkins@opennodecloud.com> - 0.8.3-1.el7
- New upstream release

* Wed Jun 6 2018 Jenkins <jenkins@opennodecloud.com> - 0.8.2-1.el7
- New upstream release

* Thu May 10 2018 Jenkins <jenkins@opennodecloud.com> - 0.8.1-1.el7
- New upstream release

* Fri Mar 23 2018 Jenkins <jenkins@opennodecloud.com> - 0.8.0-1.el7
- New upstream release

* Mon Feb 26 2018 Jenkins <jenkins@opennodecloud.com> - 0.7.5-1.el7
- New upstream release

* Fri Feb 16 2018 Jenkins <jenkins@opennodecloud.com> - 0.7.4-1.el7
- New upstream release

* Sun Feb 11 2018 Jenkins <jenkins@opennodecloud.com> - 0.7.3-1.el7
- New upstream release

* Sat Feb 3 2018 Jenkins <jenkins@opennodecloud.com> - 0.7.2-1.el7
- New upstream release

* Tue Jan 30 2018 Jenkins <jenkins@opennodecloud.com> - 0.7.1-1.el7
- New upstream release

* Mon Dec 18 2017 Jenkins <jenkins@opennodecloud.com> - 0.7.0-1.el7
- New upstream release

* Mon Dec 18 2017 Victor Mireyev <victor@opennodecloud.com> - 0.6.0-1.el7
- Initial version of the package.
