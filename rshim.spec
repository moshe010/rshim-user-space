# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2019 Mellanox Technologies. All Rights Reserved.
#

Name: rshim
Version: 2.0
Release: 1%{?dist}
Summary: User-space driver for Mellanox BlueField SoC

License: GPLv2

URL: https://github.com/mellanox/rshim-user-space
Source0: https://github.com/mellanox/rshim-user-space/archive/%{name}-%{version}.tar.gz

Obsoletes: %{name} < 2.0

BuildRequires: gcc, autoconf, automake
BuildRequires: pkgconfig(libpci), pkgconfig(libusb-1.0), pkgconfig(fuse)

%global with_systemd %(if ( test -d "%{_unitdir}" > /dev/null); then echo -n '1'; else echo -n '0'; fi)

%description
This is the user-space driver to access the BlueField SoC via the rshim
interface. It provides ways to push boot stream, debug the target or login
via the virtual console or network interface.

%prep
rm -fr %{name}-%{version}
mkdir %{name}-%{version}
tar -axf %{SOURCE0} -C %{name}-%{version} --strip-components 1
%setup -q -D -T

%build
./bootstrap.sh
%configure
make

%install
%makeinstall -C src INSTALL_DIR="%{buildroot}%{_bindir}"
%if "%{with_systemd}" == "1"
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 0644 bfrshim.service %{buildroot}%{_unitdir}
%endif
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -m 0644 man/bfrshim.1 %{buildroot}%{_mandir}/man1
%__spec_install_post

%post
%if "%{with_systemd}" == "1"
  systemctl daemon-reload
  systemctl enable bfrshim.service
%endif

%preun
%if "%{with_systemd}" == "1"
systemctl stop bfrshim
%else
killall -9 bfrshim
%endif

%files
%license LICENSE
%defattr(-,root,root,-)
%%doc README.md
%if "%{with_systemd}" == "1"
%{_unitdir}/bfrshim.service
%endif
%{_bindir}/bfrshim
%{_mandir}/man1/bfrshim.1.gz

%changelog
* Fri Mar 13 2020 Liming Sun <lsun@mellanox.com> - 2.0-1
- Update the spec file according to fedora packaging-guidelines
* Mon Dec 16 2019 Liming Sun <lsun@mellanox.com>
- Initial packaging
