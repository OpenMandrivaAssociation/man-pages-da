%define LANG da
%define name man-pages-%LANG
%define version 0.1.1
%define release %mkrel 6

Summary: Danish man pages from the Linux Documentation Project
Name: %{name}
Version: %{version}
Release: %{release}
License: Distributable
Group: System/Internationalization
Patch: manpages-da-0.1.1-manpath.patch
URL: http://www.sslug.dk/locale/man-sider/
Source: http://www.sslug.dk/locale/man-sider/manpages-da-%version.tar.bz2
BuildRoot: %_tmppath/%name-root
BuildRequires: man => 1.5j-8mdk
Requires: locales-%LANG
Requires: man => 1.5j-8mdk 
BuildRequires: sed grep man
Autoreq: false
BuildArch: noarch

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Danish.  The man pages are
organized into the following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, /etc/passwd,
                    nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)

%prep
%setup -q -n manpages-da-%{version}
%patch -p1

%build

%install
rm -fr $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT/usr install

LANG=%LANG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LANG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron << EOF
#!/bin/bash
LANG=%LANG /usr/sbin/makewhatis %_mandir/%LANG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LANG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LANG


%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%LANG, if there isn't any man page
   ## directory /%_mandir/%LANG
   if [ ! -d %_mandir/%LANG ] ; then
       /bin/rm -rf /var/catman/%LANG
   fi
fi


%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc læsmig AUTHORS ChangeLog
%dir %_mandir/%LANG
%dir /var/cache/man/%LANG
%config(noreplace) /var/cache/man/%LANG/whatis
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LANG.cron
%_mandir/%LANG/*

