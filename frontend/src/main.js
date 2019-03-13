import Vue from 'vue'
import VueAnalytics from 'vue-analytics'

import App from './App'
import router from './router'

import {
  Pagination, Dialog, Autocomplete, Dropdown,
  DropdownMenu, DropdownItem, Menu, Submenu,
  MenuItem, MenuItemGroup, Input, InputNumber,
  Radio, RadioGroup, RadioButton, Checkbox,
  CheckboxButton, CheckboxGroup, Switch,
  Select, Option, OptionGroup, Button, ButtonGroup,
  Table, TableColumn, Popover, Tooltip, Breadcrumb,
  BreadcrumbItem, Form, FormItem, Tabs,
  TabPane, Tag, Alert, Slider, Icon, Row,
  Col, Upload, Progress, Badge, Card, Steps, Step,
  Carousel, CarouselItem, Collapse, CollapseItem,
  Cascader, Transfer, Container, Header, Aside,
  Main, Footer, Loading, MessageBox, Message, Notification
} from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css'
import 'element-ui/lib/theme-chalk/display.css';
import enLocale from 'element-ui/lib/locale/lang/en'

Vue.config.productionTip = false;

Vue.use(Pagination, {enLocale});
Vue.use(Dialog, {enLocale});
Vue.use(Autocomplete, {enLocale});
Vue.use(Dropdown, {enLocale});
Vue.use(DropdownMenu, {enLocale});
Vue.use(DropdownItem, {enLocale});
Vue.use(Menu, {enLocale});
Vue.use(Submenu, {enLocale});
Vue.use(MenuItem, {enLocale});
Vue.use(MenuItemGroup, {enLocale});
Vue.use(Input, {enLocale});
Vue.use(InputNumber, {enLocale});
Vue.use(Radio, {enLocale});
Vue.use(RadioGroup, {enLocale});
Vue.use(RadioButton, {enLocale});
Vue.use(Checkbox, {enLocale});
Vue.use(CheckboxButton, {enLocale});
Vue.use(CheckboxGroup, {enLocale});
Vue.use(Switch, {enLocale});
Vue.use(Select, {enLocale});
Vue.use(Option, {enLocale});
Vue.use(OptionGroup, {enLocale});
Vue.use(Button, {enLocale});
Vue.use(ButtonGroup, {enLocale});
Vue.use(Table, {enLocale});
Vue.use(TableColumn, {enLocale});
Vue.use(Popover, {enLocale});
Vue.use(Tooltip, {enLocale});
Vue.use(Breadcrumb, {enLocale});
Vue.use(BreadcrumbItem, {enLocale});
Vue.use(Form, {enLocale});
Vue.use(FormItem, {enLocale});
Vue.use(Tabs, {enLocale});
Vue.use(TabPane, {enLocale});
Vue.use(Tag, {enLocale});
Vue.use(Alert, {enLocale});
Vue.use(Slider, {enLocale});
Vue.use(Icon, {enLocale});
Vue.use(Row, {enLocale});
Vue.use(Col, {enLocale});
Vue.use(Upload, {enLocale});
Vue.use(Progress, {enLocale});
Vue.use(Badge, {enLocale});
Vue.use(Card, {enLocale});
Vue.use(Steps, {enLocale});
Vue.use(Step, {enLocale});
Vue.use(Carousel, {enLocale});
Vue.use(CarouselItem, {enLocale});
Vue.use(Collapse, {enLocale});
Vue.use(CollapseItem, {enLocale});
Vue.use(Cascader, {enLocale});
Vue.use(Transfer, {enLocale});
Vue.use(Container, {enLocale});
Vue.use(Header, {enLocale});
Vue.use(Aside, {enLocale});
Vue.use(Main, {enLocale});
Vue.use(Footer, {enLocale});

Vue.use(Loading.directive, {enLocale});

Vue.prototype.$loading = Loading.service;
Vue.prototype.$msgbox = MessageBox;
Vue.prototype.$alert = MessageBox.alert;
Vue.prototype.$confirm = MessageBox.confirm;
Vue.prototype.$prompt = MessageBox.prompt;
Vue.prototype.$notify = Notification;
Vue.prototype.$message = Message;

Vue.filter('formatDate', function (value) {
  if (value) {
    let date = new Date(value);
    let options = {
      year: '2-digit', month: '2-digit',
      day: '2-digit', hour12: false,
      hour: '2-digit', minute: '2-digit'
    };
    return date.toLocaleDateString("en-US", options)
  }
});


Vue.use(VueAnalytics, {
  id: 'UA-136103230-1'
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {App},
  template: '<App/>'
});
