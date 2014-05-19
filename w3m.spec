# TODO add option to remove dependencies

%define gcversion gc6.3
%define Summary   Pager that can also be used as textbased webbrowser

Summary:        %{Summary}
Name:           w3m
Version:        0.5.3
Release:        2
Group:          Networking/WWW
License:        MIT
URL:            http://w3m.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/w3m/%{name}-%{version}.tar.gz
Source2:        w3mconfig
Patch0:         w3m-0.4.1-helpcharset.patch
Patch2:         w3m-0.5.1-gcc4.patch
# String literal fix - AdamW 2008/12
Patch4:		w3m-0.5.2-literal.patch
Patch6:		w3m-0.5.3.voidmain.patch
Patch7:		w3m-0.5.3.filehandle.patch
Patch8:		w3m-0.5.3.opts.patch

# w3mimgdisplay need to be linked with -lX11 to build against gcc 4.5
# https://sourceforge.net/tracker/?func=detail&aid=3126430&group_id=39518&atid=425441
Patch101:	%{name}-rh566101_Fix-DSO-X11.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=604864
# verify SSL certificates by default. SSL support really is pointless
# without doing that. Also disable use of SSLv2 by default as it's 
# insecure, deprecated, dead since last century.
# https://sourceforge.net/tracker/?func=detail&aid=3595801&group_id=39518&atid=425441
Patch102:	%{name}-0.5.2-ssl_verify_server_on.patch

# Resolves a bug of when given following command w3m crashes
# w3m https://www.example.coma
# but following command works fine by giving can't load error
# w3m http://www.example.coma
# https://sourceforge.net/tracker/?func=detail&aid=3595167&group_id=39518&atid=425441
Patch104:	%{name}-rh707994-fix-https-segfault.patch

#https://sourceforge.net/tracker/?group_id=39518&atid=425441
Patch105:	%{name}-0.5.3-parallel-make.patch

#https://bugzilla.redhat.com/show_bug.cgi?id=1038009
Patch107:	%{name}-0.5.3-FTBFS-sys-errlist.patch

Provides:       webclient
BuildRequires:  gpm-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:  imlib-devel >= 1.9.8
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig
#BuildRequires:  termcap-devel
BuildRequires:  ungif-devel
buildrequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
buildrequires:	gc-devel

%description
W3m is a text-based web browser as well as a pager like `more' or
`less'. With w3m you can browse web pages through a terminal emulator
window (xterm, rxvt or something like that). Moreover, w3m can be used
as a text formatting tool which typesets HTML into plain text. w3m also
provides w3mman which is a great manpage browser.

%prep
%setup -q
%patch0 -p1
%patch2 -p1
%patch4 -p1 -b .literal
%patch6 -p1 -b .voidmain
%patch7 -p1 -b .filehandle
%patch8 -p1 -b .opts

%patch101 -p0
%patch102 -p1
%patch104 -p0
%patch105 -p1
%patch107 -p1

#rm -rf gc

cp -a %{SOURCE2} w3mconfig

%build
rm -rf doc{,-jp}/CVS
sed -i s/showaudio/mplayer/ config.h.in

%{configure2_5x} \
                --with-browser=%{_bindir}/www-browser \
                --with-editor=%{_bindir}/vi \
                --with-mailer=/bin/mail \
                --with-termlib=ncurses \
                --enable-alarm \
                --enable-ansi-color \
                --enable-bgcolor \
                --enable-color \
                --enable-cookie \
                --enable-dict \
                --enable-digest-auth \
                --enable-external-uri-loader \
                --enable-gopher \
                --enable-help-cgi \
                --enable-history \
                --enable-image=x11,fb \
                --enable-ipv6 \
                --disable-japanese \
                --enable-keymap=w3m \
                --enable-menu \
                --enable-mouse \
                --enable-nntp \
                --enable-sslverify \
                --enable-w3mmailer \
                --disable-xface \
                --enable-m17n \
                --enable-unicode \
                --with-charset=UTF-8 \
                --with-gc=`pwd`/gc

echo '#define HAVE_SYS_ERRLIST' >> config.h

%make

%install
%makeinstall_std

install -m644 doc-jp/w3m.1 -D %{buildroot}/%{_mandir}/ja_JP.ujis/man1/w3m.1
install -m644 doc/w3m.1 -D %{buildroot}/%{_mandir}/man1/w3m.1

install -m644 w3mconfig -D %{buildroot}%{_sysconfdir}/w3m/config

%find_lang %{name} --with-man

%files -f %{name}.lang
%defattr(-,root,root)
%doc README doc w3mhelp-lynx_*
%lang(ja) %doc doc-jp 
%dir %{_sysconfdir}/w3m
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/w3m/config
%attr(0755,root,root) %{_bindir}/*
%{_libexecdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
