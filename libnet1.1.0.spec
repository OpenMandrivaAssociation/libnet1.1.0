%define	major	1.1.0
%define	libname %mklibname net %{major}

Summary:	A C library for portable packet creation
Name:		libnet%{major}
Version:	1.1.0
Release:	17
License:	BSD
Group:		System/Libraries
Url:		https://www.packetfactory.net/libnet
Source0:	http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.bz2
Patch0:		libnet-1.1.0-shared.diff
Patch1:		libnet-1.1.0-format_not_a_string_literal_and_no_format_arguments.diff
Patch2:		libnet-automake-1.13.patch
BuildRequires:	libtool
BuildRequires:	libpcap-devel

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

%description	-n %{libname}-devel
This package contains the development libnet library and its header
files.

%prep
%setup -qn Libnet-latest
%autopatch -p1

# cvs cleanup
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
	if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# fix file permissions
chmod 644 README doc/CHANGELOG*
rm -rf autom4te.cache
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake --add-missing

export LIBNET_CONFIG_CFLAGS="-I%{_includedir}/libnet"
export CFLAGS="%{optflags} -fPIC -Wall"

%build
%configure2_5x \
	--disable-static

%make CFLAGS="%{optflags} -fPIC -Wall"

# still we need to make sure the soname is 1.1.0, so..., make the shared lib the hard way
gcc -Wl,-soname,libnet.so.%{major} -shared %{optflags} -fPIC -o libnet.so.%{major} src/*.o

%install
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

%files -n %{libname}
%{_libdir}/libnet.so.%{major}

%files -n %{libname}-devel
%doc README doc/CHANGELOG* doc/COPYING
%{_bindir}/*
%{_libdir}/lib*.so
%{_includedir}/*.h
%dir %{_includedir}/libnet
%{_includedir}/libnet/*.h
%{_mandir}/man*/*

