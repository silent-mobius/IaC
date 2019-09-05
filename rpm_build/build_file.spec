Name:           chs4linux
Version:        4.1.3
Release:        1%{?dist}
Summary:        An Advance Tool Linux Server Hardening
License:        Propaitery
URL:            https://calcomsoftware.com
Source0:        chs4linux-4.1.3.tar.gz
Requires:       bash
Requires:       audit
Requires:       procps
Requires:       psacct
Requires:       nc
Requires:       rsync
Requires:       setools-console
BuildArch:      noarch

%description
Advanced hardening tool for RH Linux systems

%prep
#%setup


%install

mkdir -p $RPM_BUILD_ROOT
cp -R * $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/chs4linux/*

%changelog
* Thu Sep 5 2019    Alex M. Schapelle alex@vaiolabs.com 4.1.3
- Initial rpm release
