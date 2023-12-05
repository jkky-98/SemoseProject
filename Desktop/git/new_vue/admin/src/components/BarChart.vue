<template>
  <Bar
    :options="chartOptions"
    :data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
  />
</template>

<script>
import { Bar } from "vue-chartjs";
import { mapState } from "vuex";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "BarChart",
  components: { Bar },
  computed: {
    ...mapState({
      myAddress: "address",
      buttons: "buttons",
      zickbang_point: "zickbang_point",
      data: "receivedData",
      data_info: "receivedData_info",
    }),
  },
  props: {
    chartId: {
      type: String,
      default: "bar-chart",
    },
    datasetIdKey: {
      type: String,
      default: "label",
    },
    width: {
      type: Number,
      default: 1000,
    },
    height: {
      type: Number,
      default: 930,
    },
    cssClasses: {
      default: "",
      type: String,
    },
    styles: {
      type: Object,
      default: () => {},
    },
    plugins: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      chartOptions: {
        responsive: true,
        maintainAspectRatio: true,
        legend: {
          labels: {
            fontColor: "red",
            fontSize: 18,
          },
          color: "white",
        },
        indexAxis: "y",
        scales: {
          y: {
            ticks: {
              color: "white", // y 축의 텍스트 색상을 여기서 변경할 수 있습니다.
            },
            title: {
              display: true,
              text: "시설",
              color: "white",
              font: {
                size: 10,
              },
            },
          },
          x: {
            ticks: {
              color: "white", // x 축의 텍스트 색상을 여기서 변경할 수 있습니다.
            },
            title: {
              display: true,
              text: "거리(분)",
              color: "white",
              font: {
                size: 10,
              },
            },
          },
        },
      },
      chartData: {
        labels: ["스타벅스", "아주대학교", "이마트"],
        datasets: [
          {
            label: "Your Store List",
            backgroundColor: "#f87979",
            data: [14, 7, 12],
          },
        ],
      }, // chartData를 빈 객체로 초기화합니다.
    };
  },
  mounted() {
    // 차트가 처음 마운트될 때 차트 객체를 참조합니다.
    this.$nextTick(() => {
      this.chart = this.$refs.myChart;
    });
  },
  watch: {
    data_info: {
      deep: true,
      handler(newDataInfo) {
        if (newDataInfo && newDataInfo.info_store) {
          // info_store 데이터를 차트 데이터로 변환하여 할당합니다.
          this.chartData = this.convertInfoStoreToChartData(
            newDataInfo.info_store
          );
          this.$nextTick(() => {
            if (this.chart) {
              this.chart.update();
            }
          });
        }
      },
    },
  },
  methods: {
    convertInfoStoreToChartData(infoStore) {
      return {
        labels: infoStore.map((item) => item.name), // 이름
        datasets: [
          {
            label: "Your Store List",
            backgroundColor: "#f87979",
            data: infoStore.map((item) => item.distance), // 거리 데이터
          },
        ],
      };
    },
  },
  // ... (mounted, 다른 메서드 등은 그대로 둬요)
};
</script>
