{{{$version := printf "%s.%s.%s" .major .minor .patch }}}
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global _buildhost build-ol%{?oraclelinux}-%{?_arch}.oracle.com
%global _name	node-exporter
%global package_name	    github.com/prometheus/node_exporter
%global golang_version      1.23.0

Name:           %{_name}
Version:        {{{$version}}}
Release:        1%{?dist}
Summary:        Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.
License:        Apache 2.0
Url:            https://github.com/prometheus/node_exporter
Source:         %{name}-%{version}.tar.bz2
Source1:        node_exporter.sysconfig
Source2:        node_exporter.service
Vendor:         Oracle America
BuildRequires:  golang >= %{golang_version}
Requires(post): systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
Exporter for machine metrics. Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%package -n %{_name}-container-bin
Summary: Prometheus node_exporter binary without systemd files. Exporter for machine metrics. node-exporter package without systemd files.

%description -n %{_name}-container-bin
Exporter for machine metrics. Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors. node-exporter package without systemd files.

%prep
%setup -q -n %{name}-%{version}

%build
export GOPATH=$(go env GOPATH)
GOPATH_SRC=$GOPATH/src/%{package_name}
%__mkdir_p $GOPATH_SRC
%__mkdir_p %{_builddir}/%{name}-%{version}/output/bin
%__rm -r $GOPATH_SRC
%__ln_s $PWD $GOPATH_SRC

pushd $GOPATH_SRC
cd ${GOPATH_SRC}
GIT_REVISION={{{.commit_hash}}}
BUILD_USER=${BUILD_USER:-"${USER}@${HOSTNAME}"}
BUILD_DATE=${BUILD_DATE:-$( date +%Y%m%d-%H:%M:%S )}
GO_VERSION=$(go version | sed -e 's/^[^0-9.]*\([0-9.]*\).*/\1/' )
ldflags="
  -X github.com/prometheus/common/version.Version=v%{version}
  -X github.com/prometheus/common/version.Revision=${GIT_REVISION}
  -X github.com/prometheus/common/version.Branch=%{version}
  -X github.com/prometheus/common/version.BuildUser=${BUILD_USER}
  -X github.com/prometheus/common/version.BuildDate=${BUILD_DATE}
  -X github.com/prometheus/common/version.GoVersion=${GO_VERSION}"
go build -v -o %{_builddir}/%{name}-%{version}/output/bin/%{_name} \
    -ldflags "${ldflags}"
popd

%install
install -d -m 755 %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir}/ %{_builddir}/%{name}-%{version}/output/bin/*
install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 0660 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{_name}
install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{_name}.service

%post -n %{name}
%systemd_post %{_name}.service

%preun -n %{name}
%systemd_preun %{_name}.service

%postun -n %{name}
%systemd_postun %{_name}.service

%files -n %{name}
%license LICENSE THIRD_PARTY_LICENSES.txt NOTICE olm/SECURITY.md
%doc docs CHANGELOG.md CONTRIBUTING.md README.md
%{_bindir}/%{_name}
%{_unitdir}/%{_name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{_name}

%files -n %{name}-container-bin
%license LICENSE THIRD_PARTY_LICENSES.txt NOTICE olm/SECURITY.md
%doc docs CHANGELOG.md CONTRIBUTING.md README.md
%{_bindir}/%{_name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{_name}

%clean
rm -fr %{buildroot}
rm -fr %{_builddir}/%{name}-%{version}

%changelog
* {{{.changelog_timestamp}}} - {{{$version}}}-1
- Added Oracle Specific Build Files.
