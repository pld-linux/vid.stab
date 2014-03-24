#
# Conditional build:
%bcond_with	sse2	# use SSE2 instructions
#
%ifarch pentium4 %{x8664}
%define	with_sse2	1
%endif
Summary:	Vid.Stab - video stabilization library
Summary(pl.UTF-8):	Vid.Stab - biblioteka do stabilizacji obrazu
Name:		vid.stab
Version:	0.98
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: http://public.hronopik.de/vid.stab/download.php
Source0:	https://github.com/georgmartius/vid.stab/tarball/release-%{version}?/%{name}-%{version}.tar.gz
# Source0-md5:	809c758324c8a900faedffe81f30fe9e
Patch0:		%{name}-lib64.patch
URL:		http://public.hronopik.de/vid.stab/
BuildRequires:	cmake >= 2.6
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

%description devel
Header files for vid.stab library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki vid.stab.

%prep
%setup -q -n georgmartius-%{name}-430b4cf
%patch0 -p1

%build
install -d build
cd build
%cmake \
	%{!?with_sse:-DSSE2_FOUND=OFF} \
	..
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
%doc Changelog LICENSE README Todo
%attr(755,root,root) %{_libdir}/libvidstab.so.0.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvidstab.so
%{_includedir}/vid.stab
%{_pkgconfigdir}/vidstab.pc
