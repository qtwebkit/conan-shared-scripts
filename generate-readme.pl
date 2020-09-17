#!/usr/bin/env perl

use Config::Tiny;
use Data::Section::Simple qw(get_data_section);
use Text::Template::Simple;

use strict;
use warnings;

sub write_file {
    my ($name, $hash) = @_;
    #my $template = Text::Template->new(TYPE => 'STRING', SOURCE => get_data_section($name));
    open my $fh, '>', $name;
    my $tts = Text::Template::Simple->new();
    print $fh $tts->compile(get_data_section($name), [ %$hash ]);
    close $fh;
}


my $config = Config::Tiny->read('build.cfg');
write_file('README.md', $config->{package});
write_file('LICENSE', {});


__DATA__

@@ README.md
<% my %p = @_; %>
## Package Status

AppVeyor | GitHub Actions | Bintray
-------- | -------------- | -------
<% if (-e 'appveyor.yml') { %>[![AppVeyor Status](https://ci.appveyor.com/api/projects/status/github/qtwebkit/conan-<%= $p{name} %>?svg=true)](https://ci.appveyor.com/project/annulen/conan-<%= $p{name} %>) | <% } else { %> - | <% } %><% if (-e '.github/workflows/conan.yml') { %>[![GitHub Actions Status](https://github.com/qtwebkit/conan-<%= $p{name} %>/workflows/conan/badge.svg)](https://github.com/qtwebkit/conan-<%= $p{name} %>/actions) | <% } else { %> - | <% } %>[![Bintray](https://api.bintray.com/packages/qtproject/conan/<%= $p{name} %>%3Aqtproject/images/download.svg)](https://bintray.com/qtproject/conan/<%= $p{name} %>%3Aqtproject/_latestVersion)

## General Information

This repository is used to build recipe from [conan-center-index](https://github.com/conan-io/conan-center-index/tree/master/recipes/<%= $p{name} %>)
with options and compilers required by QtWebKit project. It contains only CI build
instructions and patches to original recipe which might be occasionally required.

Any issues related to building QtWebKit should be submitted to
[QtWebKit issue tracker](https://github.com/qtwebkit/qtwebkit/issues).
All feedback on this recipe which is not related to QtWebKit build issues should be
submitted to [upstream issue tracker](https://github.com/conan-io/conan-center-index/issues).

## Conan Information

Conan packages can be found in our [Bintray repository](https://bintray.com/qtproject/conan).
Primary intent of these packages is to support building QtWebKit on various platforms.
While it's possible that you can find these packages useful for different purposes,
build options and set of platforms and compilers may be changed in future without notice.


@@ LICENSE
Copyright (C) 2020 Konstantin Tokarev <annulen@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
