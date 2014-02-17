# TODO add option to remove dependencies

%define gcversion gc6.3
%define Summary   Pager that can also be used as textbased webbrowser

Summary:        %{Summary}
Name:           w3m
Version:        0.5.3
Release:        1
Group:          Networking/WWW
License:        MIT
URL:            http://w3m.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/w3m/%{name}-%{version}.tar.gz
Source2:        w3mconfig
Patch0:         w3m-0.4.1-helpcharset.patch
Patch2:         w3m-0.5.1-gcc4.patch
# String literal fix - AdamW 2008/12
Patch4:		w3m-0.5.2-literal.patch
patch6:		w3m-0.5.3.voidmain.patch
patch7:		w3m-0.5.3.filehandle.patch
patch8:		w3m-0.5.3.opts.patch
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
                --enable-image \
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
                --with-gc=`pwd`/gc \
								LIBS="-lX11"

echo '#define HAVE_SYS_ERRLIST' >> config.h

make

%install
install -d %{buildroot}/{%{_bindir},{%{_datadir},%{_libdir}}/%{name},%{_mandir}/{,ja_JP.ujis}/man1}

%{makeinstall_std}

install -m0644 doc-jp/w3m.1 %{buildroot}/%{_mandir}/ja_JP.ujis/man1
install -m0644 doc/w3m.1 %{buildroot}/%{_mandir}/man1

install -d %{buildroot}%{_sysconfdir}/w3m
install -m0644 w3mconfig %{buildroot}%{_sysconfdir}/w3m/config

rm -rf %{buildroot}/%{_mandir}/ja*

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README doc doc-jp w3mhelp-lynx_*
%dir %{_sysconfdir}/w3m
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/w3m/config
%attr(0755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
