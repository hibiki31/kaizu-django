import Vue from 'vue'
import VueRouter from 'vue-router'
import ItemList from '../views/ItemList.vue'
import ItemListCard from '../views/ItemListCard.vue'
import Transaction from '../views/Transaction.vue'
import CategoryList from '../views/CategoryList.vue'
import WalletList from '../views/WalletList.vue'
import Summary from '../views/Summary.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'ItemList',
    meta: { title: 'Kaizu' },
    component: ItemList
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
