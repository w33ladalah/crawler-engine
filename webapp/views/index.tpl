<!DOCTYPE html>
<!-- 
TEMPLATE NAME : Adminre backend
VERSION : 1.2.0
AUTHOR : JohnPozy
AUTHOR URL : http://themeforest.net/user/JohnPozy
EMAIL : pampersdry@gmail.com
LAST UPDATE: 23/06/2014

** A license must be purchased in order to legally use this template for your project **
** PLEASE SUPPORT ME. YOUR SUPPORT ENSURE THE CONTINUITY OF THIS PROJECT **
-->
<html class="backend">
<!-- START Head -->
<head>
    <!-- START META SECTION -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Adminre backend</title>
    <meta name="author" content="pampersdry.info">
    <meta name="description" content="Adminre is a clean and flat backend and frontend theme build with twitter bootstrap 3.1.1">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">

    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="/assets/image/touch/apple-touch-icon-144x144-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/assets/image/touch/apple-touch-icon-114x114-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/assets/image/touch/apple-touch-icon-72x72-precomposed.png">
    <link rel="apple-touch-icon-precomposed" href="/assets/image/touch/apple-touch-icon-57x57-precomposed.png">
    <link rel="shortcut icon" href="/assets/image/favicon.ico">
    <!--/ END META SECTION -->

    <!-- START STYLESHEETS -->
    <!-- Plugins stylesheet : optional -->

    <link rel="stylesheet" href="/assets/plugins/selectize/css/selectize.min.css">
    <!--/ Plugins stylesheet -->

    <!-- Application stylesheet : mandatory -->
    <link rel="stylesheet" href="/assets/library/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="/assets/stylesheet/layout1.css">
    <link rel="stylesheet" href="/assets/stylesheet/uielement.min.css">
    <!--/ Application stylesheet -->
    <!-- END STYLESHEETS -->

    <!-- START JAVASCRIPT SECTION - Load only modernizr script here -->
    <script src="/assets/library/modernizr/js/modernizr.min.js"></script>
    <!--/ END JAVASCRIPT SECTION -->
</head>
<!--/ END Head -->

<!-- START Body -->
<body>
    <!-- START Template Header -->
    <header id="header" class="navbar navbar-fixed-top">
        <!-- START navbar header -->
        <div class="navbar-header">
            <!-- Brand -->
            <a class="navbar-brand" href="javascript:void(0);">
                <span class="logo-figure"></span>
                <span class="logo-text"></span>
            </a>
            <!--/ Brand -->
        </div>
        <!--/ END navbar header -->

        <!-- START Toolbar -->
        <div class="navbar-toolbar clearfix">
            <!-- START Left nav -->
            <ul class="nav navbar-nav navbar-left">
                <!-- Sidebar shrink -->
                <li class="hidden-xs hidden-sm">
                    <a href="javascript:void(0);" class="sidebar-minimize" data-toggle="minimize" title="Minimize sidebar">
                        <span class="meta">
                            <span class="icon"></span>
                        </span>
                    </a>
                </li>
                <!--/ Sidebar shrink -->

                <!-- Offcanvas left: This menu will take position at the top of template header (mobile only). Make sure that only #header have the `position: relative`, or it may cause unwanted behavior -->
                <li class="navbar-main hidden-lg hidden-md hidden-sm">
                    <a href="javascript:void(0);" data-toggle="sidebar" data-direction="ltr" rel="tooltip" title="Menu sidebar">
                        <span class="meta">
                            <span class="icon"><i class="ico-paragraph-justify3"></i></span>
                        </span>
                    </a>
                </li>
                <!--/ Offcanvas left -->

                <!-- Message dropdown -->
                <li class="dropdown custom" id="header-dd-message">
                    <a href="javascript:void(0);" class="dropdown-toggle" data-toggle="dropdown">
                        <span class="meta">
                            <span class="icon"><i class="ico-bubbles3"></i></span>
                        </span>
                    </a>

                    <a href="page-message-rich.html" class="media border-dotted new">
                    <span class="pull-left">
                    <img src="/assets/image/avatar/{{picture}}" class="media-object img-circle" alt="">
                    </span>
                    <span class="media-body">
                    <span class="media-heading">{{name}}</span>
                    <span class="media-text ellipsis nm">{{text}}</span>

                    {{#meta.star}}<span class="media-meta"><i class="ico-star3"></i></span>{{/meta.star}}
                    {{#meta.reply}}<span class="media-meta"><i class="ico-reply"></i></span>{{/meta.reply}}
                    {{#meta.attachment}}<span class="media-meta"><i class="ico-attachment"></i></span>{{/meta.attachment}}
                    <span class="media-meta pull-right">{{meta.time}}</span>
                    </span>
                    </a>

                    </script>
                    <!--/ mustache template -->

                    <!-- Dropdown menu -->
                    <div class="dropdown-menu" role="menu">
                        <div class="dropdown-header">
                            <span class="title">Messages <span class="count"></span></span>
                            <span class="option text-right"><a href="javascript:void(0);">New message</a></span>
                        </div>
                        <div class="viewport" style="position: relative; overflow: hidden; width: auto;"><div class="dropdown-body slimscroll" style="overflow: hidden; width: auto;">
                            <!-- Search form -->
                            <form class="form-horizontal" action="">
                                <div class="has-icon">
                                    <input type="text" class="form-control" placeholder="Search message...">
                                    <i class="ico-search form-control-icon"></i>
                                </div>
                            </form>
                            <!--/ Search form -->

                            <!-- indicator -->
                            <div class="indicator inline"><span class="spinner"></span></div>
                            <!--/ indicator -->

                            <!-- Message list -->
                            <div class="media-list">
                                <a href="page-message-rich.html" class="media border-dotted read">
                                    <span class="pull-left">
                                        <img src="/assets/image/avatar/avatar1.jpg" class="media-object img-circle" alt="">
                                    </span>
                                    <span class="media-body">
                                        <span class="media-heading">Martina Poole</span>
                                        <span class="media-text ellipsis nm">Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta"><i class="ico-reply"></i></span>
                                        <span class="media-meta"><i class="ico-attachment"></i></span>
                                        <span class="media-meta pull-right">20m</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>

                                <a href="page-message-rich.html" class="media border-dotted read">
                                    <span class="pull-left">
                                        <img src="/assets/image/avatar/avatar3.jpg" class="media-object img-circle" alt="">
                                    </span>
                                    <span class="media-body">
                                        <span class="media-heading">Walter Foster</span>
                                        <span class="media-text ellipsis nm">Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta"><i class="ico-attachment"></i></span>
                                        <span class="media-meta pull-right">21h</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>

                                <a href="page-message-rich.html" class="media border-dotted read">
                                    <span class="pull-left">
                                        <img src="/assets/image/avatar/avatar4.jpg" class="media-object img-circle" alt="">
                                    </span>
                                    <span class="media-body">
                                        <span class="media-heading">Callum Santosr</span>
                                        <span class="media-text ellipsis nm">Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta pull-right">1d</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>

                                <a href="page-message-rich.html" class="media border-dotted read">
                                    <span class="pull-left">
                                        <img src="/assets/image/avatar/avatar5.jpg" class="media-object img-circle" alt="">
                                    </span>
                                    <span class="media-body">
                                        <span class="media-heading">Noelani Blevins</span>
                                        <span class="media-text ellipsis nm">Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta pull-right">2d</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>

                                <a href="page-message-rich.html" class="media border-dotted read">
                                    <span class="pull-left">
                                        <img src="/assets/image/avatar/avatar8.jpg" class="media-object img-circle" alt="">
                                    </span>
                                    <span class="media-body">
                                        <span class="media-heading">Carl Johnson</span>
                                        <span class="media-text ellipsis nm">Curabitur consequat, lectus sit amet luctus vulputate, nisi sem</span>
                                        <!-- meta icon -->
                                        <span class="media-meta"><i class="ico-attachment"></i></span>
                                        <span class="media-meta pull-right">2w</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>

                                <a href="page-message-rich.html" class="media border-dotted read">
                                    <span class="pull-left">
                                        <img src="/assets/image/avatar/avatar9.jpg" class="media-object img-circle" alt="">
                                    </span>
                                    <span class="media-body">
                                        <span class="media-heading">Tamara Moon</span>
                                        <span class="media-text ellipsis nm">Aliquam ultrices iaculis odio. Nam interdum enim non nisi. Aenean eget metus.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta"><i class="ico-attachment"></i></span>
                                        <span class="media-meta pull-right">2w</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>
                            </div>
                            <!--/ Message list -->
                        </div><div class="scrollbar" style="width: 8px; position: absolute; top: 0px; opacity: 0.4; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; z-index: 99; right: 0px; display: block; background: rgb(0, 0, 0);"></div><div class="scrollrail" style="width: 8px; height: 100%; position: absolute; top: 0px; display: block; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; opacity: 0.2; z-index: 90; right: 0px; background: rgb(51, 51, 51);"></div></div>
                    </div>
                    <!--/ Dropdown menu -->
                </li>
                <!--/ Message dropdown -->

                <!-- Notification dropdown -->
                <li class="dropdown custom" id="header-dd-notification">
                    <a href="javascript:void(0);" class="dropdown-toggle" data-toggle="dropdown">
                        <span class="meta">
                            <span class="icon"><i class="ico-bell"></i></span>
                            <span class="hasnotification hasnotification-danger"></span>
                        </span>
                    </a>

                    <!-- mustache template: used for update the `.media-list` requested from server-side -->
                    <script class="mustache-template" type="x-tmpl-mustache">

                    {{#data}}
                    <a href="javascript:void(0);" class="media border-dotted new">
                    <span class="media-object pull-left">
                    <i class="{{icon}}"></i>
                    </span>
                    <span class="media-body">
                    <span class="media-text">{{{text}}}</span>
                    <span class="media-meta pull-right">{{meta.time}}</span>
                    </span>
                    </a>
                    {{/data}}

                    </script>
                    <!--/ mustache template -->

                    <!-- Dropdown menu -->
                    <div class="dropdown-menu" role="menu">
                        <div class="dropdown-header">
                            <span class="title">Notification <span class="count"></span></span>
                            <span class="option text-right"><a href="javascript:void(0);">Clear all</a></span>
                        </div>
                        <div class="viewport" style="position: relative; overflow: hidden; width: auto;"><div class="dropdown-body slimscroll" style="overflow: hidden; width: auto;">
                            <!-- indicator -->
                            <div class="indicator inline"><span class="spinner"></span></div>
                            <!--/ indicator -->

                            <!-- Message list -->
                            <div class="media-list">
                                <a href="javascript:void(0);" class="media read border-dotted">
                                    <span class="media-object pull-left">
                                        <i class="ico-basket2 bgcolor-info"></i>
                                    </span>
                                    <span class="media-body">
                                        <span class="media-text">Duis aute irure dolor in <span class="text-primary semibold">reprehenderit</span> in voluptate.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta pull-right">2d</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>

                                <a href="javascript:void(0);" class="media read border-dotted">
                                    <span class="media-object pull-left">
                                        <i class="ico-call-incoming"></i>
                                    </span>
                                    <span class="media-body">
                                        <span class="media-text">Aliquip ex ea commodo consequat.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta pull-right">1w</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>

                                <a href="javascript:void(0);" class="media read border-dotted">
                                    <span class="media-object pull-left">
                                        <i class="ico-alarm2"></i>
                                    </span>
                                    <span class="media-body">
                                        <span class="media-text">Excepteur sint <span class="text-primary semibold">occaecat</span> cupidatat non.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta pull-right">12w</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>

                                <a href="javascript:void(0);" class="media read border-dotted">
                                    <span class="media-object pull-left">
                                        <i class="ico-checkmark3 bgcolor-success"></i>
                                    </span>
                                    <span class="media-body">
                                        <span class="media-text">Lorem ipsum dolor sit amet, <span class="text-primary semibold">consectetur</span> adipisicing elit.</span>
                                        <!-- meta icon -->
                                        <span class="media-meta pull-right">14w</span>
                                        <!--/ meta icon -->
                                    </span>
                                </a>
                            </div>
                            <!--/ Message list -->
                        </div><div class="scrollbar" style="width: 8px; position: absolute; top: 0px; opacity: 0.4; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; z-index: 99; right: 0px; display: block; background: rgb(0, 0, 0);"></div><div class="scrollrail" style="width: 8px; height: 100%; position: absolute; top: 0px; display: block; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; opacity: 0.2; z-index: 90; right: 0px; background: rgb(51, 51, 51);"></div></div>
                    </div>
                    <!--/ Dropdown menu -->
                </li>
                <!--/ Notification dropdown -->

                <!-- Search form toggler  -->
                <li>
                    <a href="javascript:void(0);" data-toggle="dropdown" data-target="#dropdown-form">
                        <span class="meta">
                            <span class="icon"><i class="ico-search"></i></span>
                        </span>
                    </a>
                </li>
                <!--/ Search form toggler -->
            </ul>
            <!--/ END Left nav -->

            <!-- START navbar form -->
            <div class="navbar-form navbar-left dropdown" id="dropdown-form">
                <form action="" role="search">
                    <div class="has-icon">
                        <input type="text" class="form-control" placeholder="Search application...">
                        <i class="ico-search form-control-icon"></i>
                    </div>
                </form>
            </div>
            <!-- START navbar form -->

            <!-- START Right nav -->
            <ul class="nav navbar-nav navbar-right">
                <!-- Profile dropdown -->
                <li class="dropdown profile">
                    <a href="javascript:void(0);" class="dropdown-toggle" data-toggle="dropdown">
                        <span class="meta">
                            <span class="avatar"><img src="/assets/image/avatar/avatar7.jpg" class="img-circle" alt=""></span>
                            <span class="text hidden-xs hidden-sm pl5">Erich Reyes</span>
                            <span class="caret"></span>
                        </span>
                    </a>
                    <ul class="dropdown-menu" role="menu">
                        <li class="pa15">
                            <h5 class="semibold hidden-xs hidden-sm">
                                <p class="nm">60%</p>
                                <small class="text-muted">Profile complete</small>
                            </h5>
                            <h5 class="semibold hidden-md hidden-lg">
                                <p class="nm">Erich Reyes</p>
                                <small class="text-muted">60% Profile complete</small>
                            </h5>
                            <div class="progress progress-xs nm mt10">
                                <div class="progress-bar progress-bar-warning" style="width: 60%">
                                    <span class="sr-only">60% Complete</span>
                                </div>
                            </div>
                        </li>
                        <li class="divider"></li>
                        <li><a href="javascript:void(0);"><span class="icon"><i class="ico-user-plus2"></i></span> My Accounts</a></li>
                        <li><a href="javascript:void(0);"><span class="icon"><i class="ico-cog4"></i></span> Profile Setting</a></li>
                        <li><a href="javascript:void(0);"><span class="icon"><i class="ico-question"></i></span> Help</a></li>
                        <li class="divider"></li>
                        <li><a href="javascript:void(0);"><span class="icon"><i class="ico-exit"></i></span> Sign Out</a></li>
                    </ul>
                </li>
                <!-- Profile dropdown -->

                <!-- Offcanvas right This menu will take position at the top of template header (mobile only). Make sure that only #header have the `position: relative`, or it may cause unwanted behavior -->
                <li class="navbar-main">
                    <a href="javascript:void(0);" data-toggle="sidebar" data-direction="rtl" rel="tooltip" title="Feed / contact sidebar">
                        <span class="meta">
                            <span class="icon"><i class="ico-users3"></i></span>
                        </span>
                    </a>
                </li>
                <!--/ Offcanvas right -->
            </ul>
            <!--/ END Right nav -->
        </div>
        <!--/ END Toolbar -->
    </header>
    <!--/ END Template Header -->

    <!-- START Template Sidebar (Left) -->
    % include('_partial/left_sidebar.tpl')
    <!--/ END Template Sidebar (Left) -->

    <!-- START Template Main -->
    % include('main.tpl')
    <!--/ END Template Main -->

    <!-- START Template Sidebar (right) -->
    % include('_partial/right_sidebar.tpl')
    <!--/ END Template Sidebar (right) -->

    <!-- START JAVASCRIPT SECTION (Load javascripts at bottom to reduce load time) -->
    <!-- Library script : mandatory -->
    <script type="text/javascript" src="/assets/library/jquery/js/jquery.min.js"></script>
    <script type="text/javascript" src="/assets/library/jquery/js/jquery-migrate.min.js"></script>
    <script type="text/javascript" src="/assets/library/bootstrap/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="/assets/library/core/js/core.min.js"></script>
    <!--/ Library script -->

    <!-- App and page level script -->
    <script type="text/javascript" src="/assets/plugins/sparkline/js/jquery.sparkline.min.js"></script><!-- will be use globaly as a summary on sidebar menu -->
    <script type="text/javascript" src="/assets/javascript/app.min.js"></script>


    <script type="text/javascript" src="/assets/plugins/flot/jquery.flot.min.js"></script>

    <script type="text/javascript" src="/assets/plugins/flot/jquery.flot.categories.min.js"></script>

    <script type="text/javascript" src="/assets/plugins/flot/jquery.flot.tooltip.min.js"></script>

    <script type="text/javascript" src="/assets/plugins/flot/jquery.flot.resize.min.js"></script>

    <script type="text/javascript" src="/assets/plugins/flot/jquery.flot.spline.min.js"></script>

    <script type="text/javascript" src="/assets/plugins/selectize/js/selectize.min.js"></script>

    <script type="text/javascript" src="/assets/javascript/pages/dashboard.js"></script>

    <!--/ App and page level script -->
    <!--/ END JAVASCRIPT SECTION -->
    
    <!--/ END Body -->

    <div id="flotTip" style="display: none; position: absolute;"></div>
</body>
<!--/ END Body -->
</html>
