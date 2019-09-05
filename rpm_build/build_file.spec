Name:           chs4linux
Version:        4.1.3
Release:        1.0.0
Summary:        An Advance Tool Linux Server Hardening

Group:          Calcom
BuildArch:      noarch
License:        Propaitery
URL:            https://calcomsoftware.com
Source0:        chs4linux-4.1.3.tar.gz
Requires:       audit,procps,psacct,nc,rsync,setools-console

%description
advanced hardening tool for RH linux systems

%prep
%setup -q -n %{name}-%{version}
%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/


%files


%changelog
* Thu Sep 5 2019    Alex M. Schapelle 4.1.3
  - Initial rpm release
