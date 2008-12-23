# TODO add option to remove dependencies

%define gcversion gc6.3
%define Summary   Pager that can also be used as textbased webbrowser

Summary:        %{Summary}
Name:           w3m
Version:        0.5.2
Release:        %mkrel 5
Group:          Networking/WWW
License:        MIT-like
URL:            http://w3m.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/w3m/%{name}-%{version}.tar.gz
Source1:        http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{gcversion}.tar.gz
Source2:        w3mconfig
Patch0:         w3m-0.4.1-helpcharset.patch
# XXX: This is against configure and not acinclude.m4 because
# XXX: acinclude.m4 is completely out of sync with aclocal.m4.
Patch1:         w3m-0.5.2-static-libgc.patch
Patch2:         w3m-0.5.1-gcc4.patch
# Hack up the syserror test. Life's too short to figure out why the
# hell it doesn't work - AdamW 2008/12
Patch3:		w3m-0.5.2-syserror.patch
# String literal fix - AdamW 2008/12
Patch4:		w3m-0.5.2-literal.patch
Provides:       webclient
#BuildRequires: gc-devel
BuildRequires:  gpm-devel
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:  imlib-devel >= 1.9.8
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  termcap-devel
BuildRequires:  ungif-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define _requires_exceptions        perl(w3mhelp-.*)

%description
W3m is a text-based web browser as well as a pager like `more' or
`less'. With w3m you can browse web pages through a terminal emulator
window (xterm, rxvt or something like that). Moreover, w3m can be used
as a text formatting tool which typesets HTML into plain text. w3m also
provides w3mman which is a great manpage browser.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .syserror
%patch4 -p1 -b .literal

rm -rf gc
tar xf %{SOURCE1}
mv %{gcversion} gc

%{__cp} -a %{SOURCE2} w3mconfig

%build
sed -i s/showaudio/mplayer/ config.h.in

(cd gc;
%{make} ABI_FLAG="%{optflags} -fPIC" gc.a
mkdir lib
ln -s ../gc.a lib/libgc.a
)

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
                --disable-kanjisymbols \
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

# kanji-symbols breaks menuboxes
# japanese-disables options and rightclick menu
%{make}

%install
rm -rf %{buildroot}

install -d %{buildroot}/{%{_bindir},{%{_datadir},%{_libdir}}/%{name},%{_mandir}/{,ja_JP.ujis}/man1}

%{makeinstall_std}

install -m0644 doc-jp/w3m.1 %{buildroot}/%{_mandir}/ja_JP.ujis/man1
install -m0644 doc/w3m.1 %{buildroot}/%{_mandir}/man1

install -d %{buildroot}%{_sysconfdir}/w3m
install -m0644 w3mconfig %{buildroot}%{_sysconfdir}/w3m/config

rm -rf %{buildroot}/%{_mandir}/ja*

%find_lang %{name}

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README doc doc-jp w3mhelp-lynx_*
%dir %{_sysconfdir}/w3m
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/w3m/config
%attr(0755,root,root) %{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
