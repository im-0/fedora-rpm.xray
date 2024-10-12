# debuginfo seems to only work with gccgo.
%global debug_package %{nil}

Name:       xray
Version:    24.9.30
Release:    1%{?dist}
Summary:    Xray, Penetrates Everything. Also the best v2ray-core, with XTLS support.

License:    MPL-2.0
URL:        https://github.com/XTLS/Xray-core
Source0:    https://github.com/XTLS/Xray-core/archive/v%{version}/Xray-core-%{version}.tar.gz

# $ GOPROXY=https://proxy.golang.org go mod vendor -v
# Contains Xray-core-%{version}/vendor/*.
Source1:    Xray-core-%{version}.go-mod-vendor.tar.xz

Source2:    xray@.service

BuildRequires:  systemd-rpm-macros
BuildRequires:  golang >= 1.21.4


%description
Xray, Penetrates Everything. Also the best v2ray-core, with XTLS support.
Fully compatible configuration.


%prep
%setup -q -D -T -b0 -n Xray-core-%{version}
%setup -q -D -T -b1 -n Xray-core-%{version}


%build
go build -v \
        -o xray \
        -trimpath \
        -ldflags "-X github.com/xtls/xray-core/core.build=%{version} -s -w -buildid=0x$(head -c20 /dev/urandom | od -An -tx1 | tr -d ' \n')" \
        ./main


%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/xray

cp %{SOURCE2} %{buildroot}/%{_unitdir}/
mv xray %{buildroot}/%{_bindir}/


%files
%{_bindir}/xray
%{_unitdir}/xray@.service
%attr(0750,root,xray) %dir %{_sysconfdir}/xray


%pre
getent group xray >/dev/null || groupadd -r xray
getent passwd xray >/dev/null || \
        useradd -r -s /sbin/nologin -d %{_sysconfdir}/xray -M \
        -c 'Xray, Penetrates Everything' -g xray xray
exit 0


%post
%systemd_post xray@.service


%preun
%systemd_preun 'xray@*.service'


%postun
%systemd_postun_with_restart 'xray@*.service'


%changelog
* Sat Oct 12 2024 Ivan Mironov <mironov.ivan@gmail.com> - 24.9.30-1
- Initial packaging
