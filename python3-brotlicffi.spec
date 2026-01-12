#
# Conditional build:
%bcond_without	system_brotli	# system brotli library
%bcond_with	tests		# unit tests (fixture data missing in sdist)

Summary:	Python 2 CFFI binding to the Brotli library
Summary(pl.UTF-8):	Wiązanie CFFI Pythona 2 do biblioteki Brotli
Name:		python3-brotlicffi
Version:	1.2.0.0
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/brotlicffi/
Source0:	https://files.pythonhosted.org/packages/source/b/brotlicffi/brotlicffi-%{version}.tar.gz
# Source0-md5:	131da94b8624542f3c36a061b1f37ab4
URL:		https://pypi.org/project/brotlicffi/
%if %{with system_brotli}
BuildRequires:	libbrotli-devel >= 1.2.0
%endif
BuildRequires:	python3-cffi >= 1.17.0
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with system_brotli}
Requires:	libbrotli >= 1.2.0
%endif
Requires:	python3-modules >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library contains Python CFFI bindings for the reference Brotli
encoder/decoder. This allows Python software to use the Brotli
compression algorithm directly from Python code.

%description -l pl.UTF-8
Ta biblioteka zawiera wiązania CFFI Pythona do wzorcowego
kodera/dekodera Brotli. Pozwala na korzystanie z algorytmu kompresji
Brotli bezpośrednio z kodu w Pythonie.

%prep
%setup -q -n brotlicffi-%{version}

%build
%if %{with system_brotli}
export USE_SHARED_BROTLI=1
%endif

%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with system_brotli}
export USE_SHARED_BROTLI=1
%endif

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY.rst LICENSE README.rst
%dir %{py3_sitedir}/brotlicffi
%{py3_sitedir}/brotlicffi/*.py
%{py3_sitedir}/brotlicffi/_brotlicffi.abi3.so
%{py3_sitedir}/brotlicffi/__pycache__
%{py3_sitedir}/brotlicffi-%{version}-py*.egg-info
