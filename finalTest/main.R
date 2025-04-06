library(plotly)
library(htmltools)
library(dplyr)
library(lubridate)
library(tidyr)
library(jsonlite)
library(jiebaR)
library(wordcloud2)
library(tidytext)

create_dashboard <- function(file_name = "result",
                             chart_width = "100%",
                             chart_height = "600px") {
  # 公用数据处理
  file <- paste0(file_name,"/stock_data.json")
  save_path <- paste0(file_name,"/result.html")
  comment_json <- paste0(file_name,"/comments.json")
  json_data <- jsonlite::fromJSON(file)
  stock_df <- json_data$result$data %>%
    mutate(
      time = as.POSIXct(m, format = "%H:%M:%S", tz = "UTC"),
      hour = hour(time),
      minute = floor(minute(time)/10)*10,
      v = as.numeric(v),
      p = as.numeric(p),
      avg_p = as.numeric(avg_p)
    )

  # 热图生成函数
  heatmap_plot <- function() {
    heatmap_data <- stock_df %>%
      group_by(hour, minute) %>%
      summarise(total_volume = sum(v), .groups = "drop") %>%
      complete(hour = 9:15, minute = seq(0, 50, 10), fill = list(total_volume = 0))

    plot_ly(heatmap_data, x = ~hour, y = ~minute, z = ~total_volume,
            type = "heatmap", colors = colorRamp(c("#f7fbff", "#2171b5"))) %>%
      layout(
        title = "成交量热图（10分钟间隔）",
        xaxis = list(title = "交易小时", tickvals = 9:15),
        yaxis = list(title = "分钟区间", tickvals = seq(0, 50, 10)),
        margin = list(t = 40)
      ) %>%
      config(displayModeBar = TRUE)
  }

  # 价格走势图生成函数
  price_plot <- function() {
    plot_ly(stock_df, x = ~time) %>%
      add_lines(y = ~p, name = "实际价格", line = list(width = 1)) %>%
      add_lines(y = ~avg_p, name = "移动均价", line = list(dash = "dot")) %>%
      layout(
        title = "价格走势分析",
        xaxis = list(title = "交易时间", tickformat = "%H:%M"),
        yaxis = list(title = "价格"),
        hovermode = "x unified",
        margin = list(t = 40)
      )
  }

  # 成交量分布图生成函数
  volume_histogram <- function() {
    plot_ly(stock_df, x = ~time, y = ~v, type = "bar",
            marker = list(color = "#6baed6", line = list(width=0))) %>%
      layout(
        title = "成交量实时分布",
        xaxis = list(title = "交易时间", tickformat = "%H:%M"),
        yaxis = list(title = "成交量"),
        bargap = 0.1,
        margin = list(t = 40)
      )
  }

    #生成词云图生成函数
word_cloud <- function(json_path) {
  comments <- fromJSON(json_path)$content
  cleaned_text <- comments %>%
    gsub("http\\S+", "", .) %>%
    gsub("[[:punct:]]", "", .) %>%
    gsub("[a-zA-Z0-9]", "", .) %>%
    gsub("\\s+", " ", .) %>%
    stringi::stri_trim_both()

  cutter <- worker(
    stop_word = "停用词.txt",
    encoding = "UTF-8"
  )

    seg_words <- segment(cleaned_text, cutter)

    word_freq <- freq(seg_words) %>%
      filter(
        nchar(char) > 1,
        !grepl("^[0-9]{2,}", char),
        freq > 1
      ) %>%
      arrange(desc(freq))
  wordcloud2(
    word_freq,
    size = 1.5,
    fontFamily = "Microsoft YaHei",
    color = "random-dark",
    backgroundColor = "white",
    shape = "circle"
  )
}
  # 组合图表
  dashboard <- tagList(
    tags$div(style = sprintf("width:%s;height:%s;", chart_width, chart_height),
             heatmap_plot()),
    tags$div(style = sprintf("width:%s;height:%s;margin-top:20px;", chart_width, chart_height),
             price_plot()),
    tags$div(style = sprintf("width:%s;height:%s;margin-top:20px;", chart_width, chart_height),
             volume_histogram()),
    tags$div(style = sprintf("width:%s;height:%s;margin-top:20px;", chart_width, chart_height),
             word_cloud(comment_json))
  )

  # 生成HTML文件
  save_html(dashboard, file = save_path,
           background = "white",
           libdir = "lib",
)

}