import Vue from 'vue'
import VueRouter from 'vue-router'
import ItemListCard from '../views/ItemListCard.vue'
import Transaction from '../views/Transaction.vue'
import CategoryList from '../views/CategoryList.vue'
import WalletList from '../views/WalletList.vue'
import Summary from '../views/Summary.vue'
import Import from '../views/Import.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Index',
    meta: { title: 'Kaizu' },
    component: ItemListCard
  },
  {
    path: '/item',
    name: 'ItemListCard',
    meta: { title: 'Kaizu' },
    component: ItemListCard
  },
  {
    path: '/transaction',
    name: 'Transaction',
    meta: { title: 'Kaizu' },
    component: Transaction
  },
  {
    path: '/category',
    name: 'CategoryList',
    meta: { title: 'Kaizu - Category' },
    component: CategoryList
  },
  {
    path: '/wallet',
    name: 'WalletList',
    meta: { title: 'Kaizu - Wallet' },
    component: WalletList
  },
  {
    path: '/import',
    name: 'Import',
    meta: { title: 'Kaizu - import' },
    component: Import
  },
  {
    path: '/summary',
    name: 'Summary',
    meta: { title: 'Kaizu - Summary' },
    component: Summary
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
