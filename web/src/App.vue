<template>
  <v-app>
    <!-- 通知 -->
    <notifications group="default" animation-type="velocity">
      <template slot="body" slot-scope="props">
        <v-alert
          :type="props.item.type"
          class="ma-3 mb-0"
          border="left"
        >
          <div class="d-flex align-center ml-3">
            <div class="body-2 mr-auto">{{ props.item.text }}</div>
          </div>
        </v-alert>
      </template>
    </notifications>
    <!-- アプリバー -->
    <v-app-bar
      app
      color="primary"
      dark
      dense
    >
      <!-- 内容 -->
      <h2>Kaizu</h2>
      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/hibiki31"
        target="_blank"
        text
      >
        <span class="mr-2">v1.3.2</span>
        <v-icon>mdi-package-variant-closed</v-icon>
      </v-btn>

      <v-btn icon v-on:click="click">
        <v-icon>mdi-cloud-download-outline</v-icon>
      </v-btn>

      <!-- タブ定義 -->
      <template v-slot:extension>
        <v-tabs align-with-title>
          <!-- タブ名 -->
          <v-tab key="tab-1" to="/item">ITEM</v-tab>
          <v-tab key="tab-2" to="/category">CATEGORY</v-tab>
          <v-tab key="tab-3" to="/wallet">WALLET</v-tab>
          <v-tab key="tab-4" to="/summary">SUMMARY</v-tab>
          <!-- 表示内容 -->
          <v-tab-item id="/item">
            <router-view v-if="activeTab === '/item'" />
          </v-tab-item>
          <v-tab-item id="/category">
            <router-view v-if="activeTab === '/category'" />
          </v-tab-item>
          <v-tab-item id="/wallet">
            <router-view v-if="activeTab === '/wallet'" />
          </v-tab-item>
          <v-tab-item id="/summary">
            <router-view v-if="activeTab === '/summary'" />
          </v-tab-item>
        </v-tabs>
      </template>
    </v-app-bar>

    <!-- ルーティングコンテンツ -->
    <v-main>
      <router-view class="pa-5" />
    </v-main>
  </v-app>
</template>

<script>
import axios from '@/axios/index'
import { saveAs } from 'file-saver'

export default {
  name: 'App',
  data: function () {
    return {
      activeTab: ''
    }
  },
  watch: {
    $route (to, from) {
      document.title = to.meta.title || 'Kaizu'
    }
  },
  methods: {
    async click () {
      saveAs(process.env.VUE_APP_API_HOST + '/api/backup', 'db')
    }
  },
  async mounted () {
    axios.interceptors.request.use(
      (config) => {
        return config
      },
      (err) => {
        return Promise.reject(err)
      }
    )
  }
}
</script>

<style>
.no-wrap {
  white-space: nowrap;
}
</style>
