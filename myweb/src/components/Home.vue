<template>
  <div>
    <div class="wrapper">
        <v-head></v-head>
        <v-sidebar></v-sidebar>
        <div class="content-box" :class="{'content-collapse':collapse}">
            <div class="content">
                <transition name="move" mode="out-in">
                    <keep-alive :include="tagsList">
                        <router-view></router-view>
                    </keep-alive>
                </transition>
                <el-backtop target=".content"></el-backtop>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import vHead from './Header.vue'
import vSidebar from './Sidebar.vue'
import bus from './bus'

export default {
  data () {
    return {
      tagsList: [],
      collapse: false
    }
  },
  components: {
    vHead,
    vSidebar
  },
  created () {
    bus.$on('collapse-content', msg => {
      this.collapse = msg
    })
  }
}
</script>
