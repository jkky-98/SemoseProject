<template>
    <div>
        <button
            v-for="(button, index) in buttons"
            :key="index"
            class="button-41"
            :class="{ 'disabled': !button.isActive }"
            @click="toggleButton(index)"
        >
            {{ button.name }}
        </button>

        <ul v-if="activeButtons.length > 0">
            <li v-for="(button, index) in activeButtons" :key="index">{{ button.name }}</li>
        </ul>
    </div>


  
</template>

<script>
export default {
  data() {
    return {
      text: 'dfasdfasdsav v',
      buttons: [
        { name: 'Button 1', isActive: false },
        { name: 'Button 2', isActive: false },
        // ... 다른 버튼들 추가
      ],
    };
  },
  computed: {
    activeButtons() {
      return this.buttons.filter(button => button.isActive);
    },
  },
  methods: {
    toggleButton(index) {
      this.buttons[index].isActive = !this.buttons[index].isActive;
    },
  },
};
</script>




<style>

/* CSS */
.button-41 {
  background-color: initial;
  background-image: linear-gradient(-180deg, #00D775, #00BD68);
  border-radius: 5px;
  box-shadow: rgba(0, 0, 0, 0.1) 0 2px 4px;
  color: #FFFFFF;
  cursor: pointer;
  display: inline-block;
  font-family: Inter,-apple-system,system-ui,Roboto,"Helvetica Neue",Arial,sans-serif;
  height: 44px;
  line-height: 44px;
  outline: 0;
  overflow: hidden;
  padding: 0 20px;
  pointer-events: auto;
  position: relative;
  text-align: center;
  touch-action: manipulation;
  user-select: none;
  -webkit-user-select: none;
  vertical-align: top;
  white-space: nowrap;
  width: 10%;
  z-index: 9;
  border: 0;
}

.button-41:hover {
  background: #00bd68;
}

.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
