
Introduction
===========


Requirements:

* gblocks module
    * To add different blocks type you page
* textile (by default) as markup language
    * You can disable it by overwriting the templates

This module is a easy way to make a simle navigation in you website, or a complexe.
Morover, integrete a systeme to create pages and his content using the admin interface.
I recomande you to use a module that permit you to edits the database content without use the admin interface (for exemple frontadmin )

Instalations
============

Simply add::

     'django.contrib.markup',
     'django_generic_flatblocks.contrib.gblocks',
     'easynav',

to your INSTALLED_APPS



Use
===

Admin
-----

In the admin create a new "ItemMenu" with:

* A http:// or https:// url
* A valide locale url (of the current projet)
* A named view (that is possible to reverse)
* A new url (see Make Generic Pages )

The Nav
=======

Main Nav
--------

Include in you template::
    
    {% load easynav_tags %}

To display the main nav use the follwing tag::
    
    {% getnav for <node> with lvl = <x>  %}


where <node> is the node tha you want to show children

* You cas use main (who is auto created)

where <x> is the display level that you want [default = 0].

* use -1 to display all the tree
* 0 for 1 level
* 1 for 2 level
* etc ...


The subnav
---------

You can use the previous tag, but you will have to hand code all your pages. A veriant tag could be use to sho the sub nav of the current page (using the path)::
    
    {% getnav for "active" %}

This tag will display the FIRST level of the sub-nav of the current page.


CSS
===

Main Nav
-------

Immagine tha your sit have this structure::
    
    - Foo
    + Bar
    |--- 1
    |--- 2
    |--- 3

The getnav tag will render you a tree like this::
    
    <ul class="menu menu-lvl-0>
        <li class="item item-lvl-0 <status>" >
            <a href="/foo">Foo</a>
        </li>
        <li class="item item-lvl-0 <status>" >
            <a href="/bar">Bar</a>
            <ul class="menu menu-lvl-1">
                <li class="item item-lvl-1 <status>" >
                    <a href="/bar/1">1</a>
                </li>V
                <li class="item item-lvl-1 <status>" >
                    <a href="/bar/2">2</a>
                </li>V
                <li class="item item-lvl-1 <status>" >
                    <a href="/bar/3">3</a>
                </li>V
            </ul>
        </li>
    </ul>

With <status> = active or inactive

* menu is a class that is present in all the <ul>
* item is present in all the <li>
* menu-lvl-x is present il all the <ul> with x equal to the current level of nav
* item-lvl-x is present il all the <li> with x equal to the current level of nav
* active and inactive is in all the <li>

Imagine that the current path is /bar/3, the nav will be::
    
    <ul class="menu menu-lvl-0>
        <li class="item item-lvl-0 inactive" >
            <a href="/foo">Foo</a>
        </li>
        <li class="item item-lvl-0 active" >
            <a href="/bar">Bar</a>
            <ul class="menu menu-lvl-1">
                <li class="item item-lvl-1 inactive" >
                    <a href="/bar/1">1</a>
                </li>V
                <li class="item item-lvl-1 inactive" >
                    <a href="/bar/2">2</a>
                </li>V
                <li class="item item-lvl-1 active" >
                    <a href="/bar/3">3</a>
                </li>V
            </ul>
        </li>
    </ul>

As you see, the active class is present in all the parent node of /bar/3


Sub Nav
-------


The sub nav will be like this (with the current page as Bar )::
    
    <ul class="submenu">
        <li class="subitem">
            <a href="/bar/1">1</a>
        </li>
        <li class="subitem">
            <a href="/bar/2">2</a>
        </li>
        <li class="subitem">
            <a href="/bar/3">3</a>
        </li>
    </ul>

The sub nav will display juste the first level.


Make Generic Pages
==================

Creation
--------

* In the admin, create a new "ItemMenu" with "Auto Create Page" True.
* Then choose the parent node (main by default)
* Complite de "View" field, (that begin with a "/" ) or leave it blank to auto create it
* Choose the type of the content that you need in you page (Images, Text, Titles , Image and Text, ...)
* choose a unique slug for it, or leave it blank to auto create it
* Order the blanks using "rank" field.

Done.

Modify Content
--------------

I recomende you to use a module that permit you to edit content 'in live' (ex : frontadmin ).
In fact, editing block using the admin is not realy easy, but you can try (in gblocks moduls)

Render
------

The render page use your base.html (herite)::
    
    {% extends "base.html" %}

THe page insert his code in the block::
    
    {% block project.body %}{% endblock %}

Each block will be encapsulate un a <div> like this::
    
    <div class="block">
        {{ block_content }}
    </div>

By default the title are in::
    
    <h2>Title</h2>

Image::
    
    <img src="{{MEDIA_URL}}{{block.image}}">

Links::
    
    <a href="{{block.link}}">{{block.link}}</a>

Text::
    
    {{ block.text|textile }}

File::
    
    <a href="{{MEDIA_URL}}{{block.file}}">File</a>



Custom
------

You can custom the render of the basique page by overwriting: *'easynav/templates/easynav/genericPage.html'*

Each block can be custom by overwriting : *'easynav/templates/include/gblocks.<type>.inc.html'*

Where <type> could be:

* Image
* Text
* Title
* ImageAndLink
* TitleAndFile
* TitleAndText
* TitleTextAndFile
* TitleTextAndImage

