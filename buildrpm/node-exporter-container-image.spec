
%global debug_package   %{nil}
%{!?registry: %global registry container-registry.oracle.com/olcne}
%global _name	node-exporter

Name:       %{_name}-container-image
Version:    1.9.1
Release:    1%{?dist}
Summary:    Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.
License:    Apache 2.0
Url:        https://github.com/prometheus/node_exporter
Source:     %{name}-%{version}.tar.bz2
Vendor:     Oracle America

%description
Exporter for machine metrics. Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%prep
%setup -q -n %{name}-%{version}

%build
%global docker_tag %{registry}/%{_name}:v%{version}
%if %{?oraclelinux} == 8
    %define dockerfile "Dockerfile"
%endif

%__rm -f .dockerignore
yum clean all
yumdownloader --destdir=${PWD}/rpms %{_name}-container-bin-%{version}-%{release}.%{_build_arch}

docker build --pull \
    --build-arg https_proxy=${https_proxy} \
    -t %{docker_tag} -f ./olm/builds/%{dockerfile} .
docker save -o %{_name}.tar %{docker_tag}

%install
%__install -D -m 644 %{_name}.tar %{buildroot}/usr/local/share/olcne/%{_name}.tar

%files
%license LICENSE NOTICE THIRD_PARTY_LICENSES.txt olm/SECURITY.md

/usr/local/share/olcne/%{_name}.tar

%changelog
* Mon Sep 15 2025 Olcne-Builder Jenkins <olcne-builder_us@oracle.com> - 1.9.1-1
- Added Oracle Specific Build Files.
