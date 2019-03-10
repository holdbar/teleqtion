import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '../components/Dashboard'
import Scrapping from '../components/Scrapping'
import Inviting from "../components/Inviting"
import Groups from "../components/Groups";
import Accounts from "../components/Accounts";
import Messaging from "../components/Messaging";
import Balance from "../components/Balance";
import PageNotFound from "../components/PageNotFound";

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/app',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/accounts',
      name: 'Accounts',
      component: Accounts
    },
    {
      path: '/groups',
      name: 'Groups',
      component: Groups
    },
    {
      path: '/scrapping',
      name: 'Scrapping',
      component: Scrapping
    },
    {
      path: '/inviting',
      name: 'Inviting',
      component: Inviting
    },
    {
      path: '/messaging',
      name: 'Messaging',
      component: Messaging
    },
    {
      path: '/balance',
      name: 'Balance',
      component: Balance
    },
    {
      path: '*',
      name: 'PageNotFound',
      component: PageNotFound
    },

  ]
})
