#
# Conditional build:
%bcond_without	openmp	# OpenMP parallelization
%bcond_with	sse2	# use SSE2 instructions
#
%ifarch pentium4 %{x8664}
%define	with_sse2	1
%endif
Summary:	Vid.Stab - video stabilization library
Summary(pl.UTF-8):	Vid.Stab - biblioteka do stabilizacji obrazu
Name:		vid.stab
Version:	1.1.1
Release:	1
License:	GPL v2+
Group:		Libraries
# also http://public.hronopik.de/vid.stab/download.php
#Source0Download: https://github.com/georgmartius/vid.stab/tags
Source0:	https://github.com/georgmartius/vid.stab/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3fb59a96f6e49e2719fd8c551eb3617a
URL:		http://public.hronopik.de/vid.stab/
BuildRequires:	cmake >= 2.8.5
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Vid.Stab is a library for stabilizing video clips.

%description -l pl.UTF-8
Vid.Stab to biblioteka do stabilizacji filmów.

%package devel
Summary:	Header files for vid.stab library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki vid.stab
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_openmp:Requires:	libgomp-devel}

%description devel
Header files for vid.stab library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki vid.stab.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{!?with_sse:-DSSE2_FOUND=OFF} \
	%{!?with_openmp:-DUSE_OMP=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog LICENSE README.md Todo
%attr(755,root,root) %{_libdir}/libvidstab.so.1.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvidstab.so
%{_includedir}/vid.stab
%{_pkgconfigdir}/vidstab.pc
