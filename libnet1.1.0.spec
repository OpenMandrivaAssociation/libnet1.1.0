%define	major 1.1.0
%define	libname %mklibname net %{major}

Summary:	A C library for portable packet creation
Name:		libnet%{major}
Version:	1.1.0
Release:	%mkrel 3
License:	BSD
Group:		System/Libraries
URL:		http://www.packetfactory.net/libnet
Source0:	http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.bz2
Patch0:		libnet-1.1.0-shared.diff
BuildPreReq:	libpcap-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information

%if "%{_lib}" != "lib"
%package -n	%{libname}
Summary:	A C library for portable packet creation
Group:		System/Libraries

%description -n %{libname}
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information
%endif

%package -n	%{libname}-devel
Summary:	Development library and header files for the libnet library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	libnet%{major}-devel = %{version}-%{release}
Provides:	net-devel = %{version}-%{release}
Provides:	%{mklibname net 1.1}-devel = %{version}-%{release}
Obsoletes:	%{mklibname net 1.1}-devel
Conflicts:	%{mklibname net 1.0.2}-devel
Conflicts:	%{mklibname net 1.1.2}-devel

%description	-n %{libname}-devel
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information

This package contains the static libnet library and its header
files.

%package -n	%{libname}-static-devel
Summary:	Static development library for the libnet library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	libnet%{major}-static-devel = %{version}-%{release}
Provides:	%{mklibname net 1.1}-devel = %{version}-%{release}
Obsoletes:	%{mklibname net 1.1}-devel
Conflicts:	%{mklibname net 1.0.2}-static-devel
Conflicts:	%{mklibname net 1.1.2}-static-devel

%description	-n %{libname}-static-devel
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information

This package contains the static libnet library.

%prep

%setup -n Libnet-latest -q
%patch0 -p1

# cvs cleanup
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# fix file permissions
chmod 644 README doc/CHANGELOG*

%build
rm -rf autom4te.cache
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --add-missing

export LIBNET_CONFIG_CFLAGS="-I%{_includedir}/libnet"
export CFLAGS="%{optflags} -fPIC -Wall"

%configure2_5x \
    --with-pf_packet=yes 

%make CFLAGS="%{optflags} -fPIC -Wall"

# still we need to make sure the soname is 1.1.0, so..., make the shared lib the hard way
gcc -Wl,-soname,libnet.so.%{major} -shared %{optflags} -fPIC -o libnet.so.%{major} src/*.o

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man3

%makeinstall_std

install -m755 libnet-config %{buildroot}%{_bindir}/

# install man pages
install -m0644 man/* %{buildroot}%{_mandir}/man3/

# fix the lib
rm -f %{buildroot}%{_libdir}/lib*.so*
install -m0755 libnet.so.%{major} %{buildroot}%{_libdir}/
ln -snf libnet.so.%{major} %{buildroot}%{_libdir}/libnet.so

# cleanup
rm -f %{buildroot}%{_libdir}/lib*.la

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README doc/CHANGELOG* doc/COPYING
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_libdir}/lib*.so
#%attr(0644,root,root) %{_libdir}/lib*.la
%attr(0644,root,root) %{_includedir}/*.h
%dir %{_includedir}/libnet
%attr(0644,root,root) %{_includedir}/libnet/*.h
%attr(0644,root,root) %{_mandir}/man*/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/lib*.a


