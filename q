[1mdiff --git a/tp_yass/themes/tp_yass2020/backend/user_create.jinja2 b/tp_yass/themes/tp_yass2020/backend/user_create.jinja2[m
[1mindex 886297a..9be81fe 100644[m
[1m--- a/tp_yass/themes/tp_yass2020/backend/user_create.jinja2[m
[1m+++ b/tp_yass/themes/tp_yass2020/backend/user_create.jinja2[m
[36m@@ -1,7 +1,7 @@[m
 {% extends "layouts/master.jinja2" %}[m
 {% from 'macros.jinja2' import generate_user_group_trees %}[m
 {% block page_css %}[m
[31m-<link href="{{ 'tp_yass:themes/default/static/css/jquery.bonsai-2.1.1.css'|static_path }}" rel="stylesheet">[m
[32m+[m[32m  <link rel="stylesheet" href="{{ 'tp_yass:themes/default/static/css/jquery.bonsai-2.1.1.css'|static_path }}">[m
 {% endblock page_css %}[m
 {% block content %}[m
 <div class="container">[m
[36m@@ -56,14 +56,14 @@[m
 </div>[m
 {% endblock content %}[m
 {% block page_js %}[m
[31m-<script src="{{ 'tp_yass:themes/default/static/js/jquery.qubit-2.0.9.js'|static_path }}"></script>[m
[31m-<script src="{{ 'tp_yass:themes/default/static/js/jquery.bonsai-2.1.1.js'|static_path }}"></script>[m
[31m-<script>[m
[31m-  $(function() {[m
[31m-    $('#root-group').bonsai({[m
[31m-      expandAll: true,[m
[31m-      createInputs: 'checkbox'[m
[32m+[m[32m  <script src="{{ 'tp_yass:themes/default/static/js/jquery.qubit-2.0.9.js'|static_path }}"></script>[m
[32m+[m[32m  <script src="{{ 'tp_yass:themes/default/static/js/jquery.bonsai-2.1.1.js'|static_path }}"></script>[m
[32m+[m[32m  <script>[m
[32m+[m[32m    $(function() {[m
[32m+[m[32m      $('#root-group').bonsai({[m
[32m+[m[32m        expandAll: true,[m
[32m+[m[32m        createInputs: 'checkbox'[m
[32m+[m[32m      });[m
     });[m
[31m-  });[m
[31m-</script>[m
[32m+[m[32m  </script>[m
 {% endblock page_js %}[m
