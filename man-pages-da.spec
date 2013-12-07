%define LNG da

Summary:	Danish man pages from the Linux Documentation Project
Name:		man-pages-%{LNG}
Version:	0.1.1
Release:	17
License:	Distributable
Group:		System/Internationalization
Url:		http://www.sslug.dk/locale/man-sider/
Source0:	http://www.sslug.dk/locale/man-sider/manpages-da-%{version}.tar.bz2
Patch0:		manpages-da-0.1.1-manpath.patch
BuildArch:	noarch
BuildRequires:	grep
BuildRequires:	man
BuildRequires:	sed
Requires:	locales-%{LNG}
Requires:	man
Autoreq:	false

%description
A large collection of man pages (reference material) from the Linux 
Documentation Project (LDP), translated to Danish.  The man pages are
organized into the following sections:

        Section 1:  User commands (intro only)
        Section 2:  System calls
        Section 3:  Libc calls
        Section 4:  Devices (e.g., hd, sd)
        Section 5:  File formats and protocols (e.g., wtmp, %{_sysconfdir}passwd,
                    nfs)
        Section 6:  Games (intro only)
        Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
        Section 8:  System administration (intro only)

%prep
%setup -qn manpages-da-%{version}
%apply_patches

%build

%install
make PREFIX=%{buildroot}/usr install

LANG=%{LNG} DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%{_mandir}/%{LNG}

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron << EOF
#!/bin/bash
LANG=%{LNG} %{_bindir}/mandb %{_mandir}/%{LNG}
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LNG}

touch %{buildroot}/var/cache/man/%{LNG}/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%{LNG}, if there isn't any man page
   ## directory /%{_mandir}/%{LNG}
   if [ ! -d %{_mandir}/%{LNG} ] ; then
       /bin/rm -rf /var/catman/%{LNG}
   fi
fi

%post
%create_ghostfile /var/cache/man/%{LNG}/whatis root root 644

%files
%doc læsmig AUTHORS ChangeLog
%dir %{_mandir}/%{LNG}
%dir /var/cache/man/%{LNG}
%ghost %config(noreplace) /var/cache/man/%{LNG}/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron
%{_mandir}/%{LNG}/*

