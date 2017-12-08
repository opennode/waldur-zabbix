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
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Wed Sep 21 2016 Jenkins <jenkins@opennodecloud.com> - 0.6.0-1.el7
- New upstream release

* Thu Sep 15 2016 Jenkins <jenkins@opennodecloud.com> - 0.5.0-1.el7
- New upstream release

* Wed Sep 7 2016 Jenkins <jenkins@opennodecloud.com> - 0.4.0-1.el7
- New upstream release

* Wed Aug 17 2016 Jenkins <jenkins@opennodecloud.com> - 0.3.2-1.el7
- New upstream release

* Fri Aug 12 2016 Jenkins <jenkins@opennodecloud.com> - 0.3.1-1.el7
- New upstream release

* Sat Jun 11 2016 Jenkins <jenkins@opennodecloud.com> - 0.3.0-1.el7
- New upstream release

* Tue Dec 8 2015 Jenkins <jenkins@opennodecloud.com> - 0.2.1-1.el7
- New upstream release

* Tue Dec 8 2015 Jenkins <jenkins@opennodecloud.com> - 0.2.0-1.el7
- New upstream release

* Mon Nov 9 2015 Juri Hudolejev <juri@opennodecloud.com> - 0.1.0-1.el7
- Initial version of the package

