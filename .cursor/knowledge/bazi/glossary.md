# Bazi Glossary - Từ Điển Thuật Ngữ

## Giới thiệu

Tài liệu này cung cấp danh sách đầy đủ các thuật ngữ chuyên ngành được sử dụng trong hệ thống Bazi, bao gồm Tử Vi, phong thủy, và các ứng dụng liên quan. Mỗi thuật ngữ được định nghĩa chi tiết với ngữ cảnh sử dụng trong thực tế.

## Các thuật ngữ cơ bản

### 1. Bát Tự (八字 - Eight Characters)

Bát Tự là hệ thống tính toán dựa trên năm yếu tố: năm, tháng, ngày, giờ sinh. Mỗi yếu tố được biểu diễn bằng một cặp Hán tự (thiên can và địa chi), tạo thành tổng cộng 8 chữ số. Đây là nền tảng cốt lõi của Bazi, dùng để phân tích vận mệnh, tính cách, và xu hướng cuộc đời một người. Hệ thống này có nguồn gốc từ kinh Dịch và được phát triển hoàn chỉnh trong các triều đại Trung Hoa.

Cấu trúc của Bát Tự bao gồm bốn cột, mỗi cột có hai chữ: một thiên can và một địa chi. Ví dụ một người sinh năm 1990 thuộc canh tuất sẽ có thiên can là "Canh" và địa chi là "Tuất". Sự kết hợp giữa can và chi tạo ra 60 liên niên, mỗi liên niên có những đặc tính và ý nghĩa riêng biệt. Trong lập trình, chúng ta cần biểu diễn cấu trúc này dưới dạng dữ liệu có thể xử lý được.

### 2. Thiên Can (天干 - Heavenly Stems)

Thiên Can là 10 nguyên tố thiên hướng, đại diện cho năng lượng vũ trụ tương tác với con người. Bao gồm: Giáp (Jia), Ất (Yi), Bính (Bing), Đinh (Ding), Mậu (Wu), Kỷ (Ji), Canh (Geng), Tân (Xin), Nhâm (Ren), Quý (Gui). Mỗi can mang một ngũ hành riêng: Giáp, Ất thuộc Mộc; Bính, Đinh thuộc Hỏa; Mậu, Kỷ thuộc Thổ; Canh, Tân thuộc Kim; Nhâm, Quý thuộc Thủy.

Trong hệ thống tính toán, mỗi thiên can có chỉ số âm dương xác định. Giáp, Bính, Mậu, Canh, Nhâm là Dương; Ất, Đinh, Kỷ, Tân, Quý là Âm. Sự tương sinh, tương khắc giữa các can tạo nên động thái của lá số. Khi phát triển phần mềm, cần xây dựng ma trận tương tác giữa các can để tính toán các chỉ số phong thủy.

### 3. Địa Chi (地支 - Earthly Branches)

Địa Chi là 12 con giáp trong vòng tròn hoàng đạo, biểu diễn cho các giai đoạn thời gian và năng lượng địa lý. Bao gồm: Tý (Rat), Sửu (Ox), Dần (Tiger), Mão (Rabbit), Thìn (Dragon), Tỵ (Snake), Ngọ (Horse), Mùi (Goat), Thân (Monkey), Dậu (Rooster), Tuất (Dog), Hợi (Pig). Mỗi chi cũng mang thuộc tính ngũ hành và âm dương riêng.

Địa chi không chỉ đơn thuần là con giáp mà còn chứa thông tin về mùa, thời tiết, và các mối quan hệ không gian. Ví dụ Mão (Mẹo) đại diện cho mùa xuân và năng lượng Mộc; Ngọ đại diện cho mùa hè và năng lượng Hỏa. Trong database, Địa Chi được lưu trữ với các trường: mã chi, tên, ngũ hành, âm dương, và giờ sinh tương ứng.

### 4. Ngũ Hành (五行 - Five Elements)

Ngũ Hành là năm nguyên tố cơ bản tạo nên vạn vật: Kim (Metal), Mộc (Wood), Thủy (Water), Hỏa (Fire), Thổ (Earth). Mỗi người, vật, sự kiện đều mang năng lượng của một hoặc nhiều hành. Hệ thống này dựa trên chu kỳ tương sinh (Kim → Thủy → Mộc → Hỏa → Thổ → Kim) và tương khắc (Kim → Mộc → Thổ → Thủy → Hỏa → Kim).

Trong phong thủy, việc cân bằng ngũ hành là yếu tố quan trọng nhất. Một người có lá số thiên về Mộc quá mạnh cần bổ sung Kim để cân bằng. Ngược lại, người thiếu Mộc cần tăng cường yếu tố này qua màu sắc, số, hướng, hoặc các vật phẩm phong thủy. Thuật toán tính toán ngũ hành cần xử lý cả chu kỳ tương sinh và tương khắc một cách chính xác.

### 5. Thập Thần (十神 - Ten Gods)

Thập Thần là mười mối quan hệ tương tác giữa ngày chủ (ngày sinh) và các can khác trong lá số. Bao gồm: Chính Ấn, Tự Ấn, Chính Quan, Tài Quan, Chính Tài, Tài Tài, Bảo Quân, Thiên Quan, Bạn Quân, Lộc Quân. Mỗi thần đại diện cho một khía cạnh cuộc sống: sự nghiệp, tài lộc, quan hệ, sức khỏe, trí tuệ.

Thập Thần được phân thành các nhóm: Ngại Thần (Ấn, Quan) và Tài Thần (Tài, Lộc). Ngại Thần mang năng lượng bảo vệ, nuôi dưỡng; Tài Thần mang năng lượng vật chất, thực dụng. Khi phân tích lá số, cần đánh giá tổng hợp các Thần để đưa ra kết luận về tính cách và vận mệnh. Đây là thuật ngữ quan trọng trong việc lập trình AI phân tích Bazi.

### 6. Cục Diện (格局 - Pattern Structure)

Cục Diện là cách sắp xếp các yếu tố trong lá số tạo thành một mô hình có ý nghĩa. Các cục diện phổ biến bao gồm: Công Thương Nghiệp (Tài Quân), Bảo Quan Tài (Ấn Quan), Tài Quan Vượng (Tài Quân), Quan Tài Kiệt (Quan Quân), Đào Hoa Tài (Hồng Loan), Thanh Balần (Thanh Long), Hắc Vận Quỷ (Hắc Vận). Mỗi cục diện có đặc điểm và ý nghĩa riêng về con đường phát triển cuộc đời.

Cục Diện không chỉ là nhãn mà còn là framework để phân tích sâu. Ví dụ Công Thương Nghiệp cho thấy người này phù hợp với kinh doanh, buôn bán; Bảo Quan Tài cho thấy người này có thể làm trong bộ máy nhà nước hoặc các tổ chức lớn. Trong hệ thống AI, cục diện là một feature quan trọng để phân loại lá số và đề xuất hướng đi phù hợp.

### 7. Vận (运 - Fate/运气 Period)

Vận là chu kỳ thời gian 10 năm thể hiện sự thay đổi của vận mệnh qua các giai đoạn khác nhau. Mỗi người trải qua nhiều Vận trong đời, mỗi Vận kéo dài 10 năm và mang một thiên can địa chi riêng. Vận được tính dựa trên lá số gốc và các quái số liên quan. Cách tính Vận là một trong những kỹ năng phức tạp nhất của Bazi.

Trong ứng dụng thực tế, người ta muốn biết Vận hiện tại của mình đang như thế nào để có quyết định đúng đắn. Vận tốt thì nên tấn công, mở rộng; Vận xấu thì nên bảo thủ, chờ thời. API cung cấp thông tin Vận cần đi kèm với giải thích và đề xuất hành động cụ thể. Đây là tính năng có giá trị cao với người dùng.

### 8. Lục Hợp (六合 - Six Combinations)

Lục Hợp là sáu cặp địa chi kết hợp tạo ra năng lượng hài hòa, bổ trợ lẫn nhau. Các cặp Lục Hợp gồm: Tý-Sửu, Dần-Hợi, Mão-Tuất, Thìn-Dậu, Tỵ-Ngọ, Mùi-Thân. Khi hai chi Lục Hợp xuất hiện trong lá số hoặc tương tác với nhau, chúng tạo ra một trạng thái năng lượng ổn định, thuận lợi cho các mối quan hệ và công việc.

Trong phong thủy, Lục Hợp được ứng dụng để xác định hướng hợp, số hợp, màu hợp với mỗi người. Ví dụ người tuổi Dần sẽ hợp với người tuổi Hợi trong các mối quan hệ làm ăn, hôn nhân. Khi phát triển tính năng tư vấn, cần tích hợp logic Lục Hợp để đề xuất các phương án tối ưu cho người dùng.

### 9. Lục Xung (六冲 - Six Conflicts)

Lục Xung là sáu cặp địa chi đối nghịch tạo ra năng lượng xung đột, mâu thuẫn. Các cặp xung gồm: Tý-Ngọ, Sửu-Mùi, Dần-Thân, Mão-Dậu, Thìn-Tuất, Tỵ-Hợi. Khi hai chi xung xuất hiện trong lá số hoặc tương tác, chúng tạo ra năng lượng bất ổn, thách thức, và cần vượt qua trong giai đoạn đó.

Lục Xung không phải lúc nào cũng xấu; trong một số trường hợp, xung còn mang ý nghĩa của sự phát triển, thay đổi, và đột phá. Tuy nhiên, nếu Vận hiện tại có nhiều xung, người ta thường được khuyên cẩn thận hơn trong các quyết định quan trọng. Phần mềm Bazi cần hiển thị rõ các cặp xung trong lá số để người dùng nhận biết và xử lý phù hợp.

### 10. Tam Hợp (三合 - Three Combinations)

Tam Hợp là nhóm ba địa chi kết hợp tạo thành năng lượng mạnh mẽ, ổn định. Các nhóm Tam Hợp gồm: Thìn-Tỵ-Sửu (Thổ Hỏa), Hợi-Mão-Mùi (Mộc Thủy), Dần-Tuất-Ngọ (Hỏa Mộc), Thân-Tỵ-Dậu (Kim). Mỗi Tam Hợp có một Thập Thần hỗ trợ gọi là Hóa hãm (tam hợp trì).

Tam Hợp thể hiện mối quan hệ hợp tác bền vững, lâu dài. Trong phong thủy, nếu một người có nhiều chi thuộc cùng một nhóm Tam Hợp, họ thường gặp may mắn trong các mối quan hệ với người cùng nhóm. Đây cũng là yếu tố để xác định hướng nhà, số xe, hoặc màu sắc may mắn.

### 11. Tứ Trụ (四柱 - Four Pillars)

Tứ Trụ là bốn cột của lá số Bazi: Năm, Tháng, Ngày, Giờ. Mỗi cột có thiên can và địa chi, tạo thành tổng cộng 8 chữ số. Tên gọi Tứ Trụ nhấn mạnh rằng đây là bốn trụ cột nền tảng, định hình toàn bộ cuộc đời con người. Thứ tự quan trọng: Năm trụ (cha, tổ tiên), Tháng trụ (sự nghiệp, bản thân), Ngày trụ (vợ/chồng, tài chính), Giờ trụ (con cái, tương lai).

Trong lập trình, Tứ Trụ được biểu diễn như một object có cấu trúc: {year: {can: string, chi: string}, month: {can: string, chi: string}, day: {can: string, chi: string}, hour: {can: string, chi: string}}. Các API phân tích lá số cần xác định rõ vai trò của từng trụ để đưa ra kết luận chính xác về các khía cạnh cuộc sống tương ứng.

### 12. Đại Vận (大运 - Major Decade Cycle)

Đại Vận là chu kỳ 10 năm thể hiện vận khí tổng thể của một giai đoạn lớn trong đời người. Đại Vận được tính dựa trên giới tính, ngày sinh, và các yếu tố trong Tứ Trụ. Mỗi người trải qua nhiều Đại Vận liên tiếp, mỗi vận kéo dài 10 năm. Đây là yếu tố quan trọng nhất để xác định thời điểm tốt/xấu trong cuộc đời.

Trong ứng dụng, người dùng muốn biết Đại Vận hiện tại của họ đang ở giai đoạn nào của chu kỳ 10 năm. Vận đầu thường là giai đoạn chuyển giao, vận giữa là đỉnh cao hoặc thấp nhất, vận cuối là chuẩn bị cho vận tiếp theo. Tính năng hiển thị Đại Vận cần kết hợp với phân tích chi tiết từng năm trong vận đó.

### 13. Tiểu Vận (小运 - Minor Year Cycle)

Tiểu Vận là chu kỳ 1 năm thể hiện vận khí của từng năm cụ thể. Tiểu Vận được tính dựa trên số dương lịch và các yếu tố Bazi. Trong khi Đại Vận cho cái nhìn tổng quan của 10 năm, Tiểu Vận cho biết chi tiết từng năm, tháng, ngày. Đây là công cụ dự báo ngắn hạn quan trọng trong Bazi.

Ứng dụng Bazi hiện đại cần cung cấp thông tin Tiểu Vận để người dùng có thể lập kế hoạch chi tiết. Ví dụ một năm có Tiểu Vận xấu có thể là năm để xây dựng nền tảng, chuẩn bị; trong khi năm tốt có thể là năm để tấn công, mở rộng. API cần trả về cả Tiểu Vận năm, tháng, và ngày để người dùng có thông tin đầy đủ.

### 14. Tuổi (年齡 - Age/Zodiac Age)

Tuổi trong Bazi không chỉ là số tuổi thông thường mà còn là con số đại diện cho năng lượng của một chu kỳ 12 năm trong vòng tròn hoàng đạo. Mỗi tuổi mang một địa chi riêng và có những đặc điểm riêng. Tuổi được sử dụng để xác định hướng hợp, màu hợp, số hợp, và các yếu tố phong thủy khác. Khi nói "tuổi Dần" là chỉ người sinh vào năm thuộc địa chi Dần.

Trong lập trình, khi xử lý thông tin tuổi, cần phân biệt giữa "tuổi Âm Lịch" (tuổi con giáp) và "tuổi tác" (số tuổi thực tế). Nhiều ứng dụng Bazi cần chuyển đổi giữa Âm Lịch và Dương Lịch để đảm bảo tính chính xác. Đây là một trong những thách thức kỹ thuật quan trọng khi xây dựng hệ thống Bazi.

### 15. Số Phận (命运 - Destiny/Fate)

Số Phận là tổng hợp tất cả các yếu tố trong Bazi để đưa ra bức tranh toàn diện về cuộc đời một người. Số Phận không phải là định mệnh cố định mà là xu hướng, tiềm năng, và các thách thức mà người đó có thể gặp. Bazi giúp con người hiểu rõ hơn về bản thân để đưa ra quyết định sáng suốt hơn, không phải để "đoán trước" tương lai một cách máy móc.

Trong hệ thống AI, Số Phận được biểu diễn như một vector đặc trưng bao gồm: cung mệnh, cung thân, ngũ hành, thập thần, cục diện, và các yếu tố tương tác. Machine Learning model được huấn luyện trên dataset lớn về các lá số và kết quả cuộc đời để đưa ra dự đoán có cơ sở khoa học hơn.

### 16. Phong Thủy (風水 - Feng Shui)

Phong Thủy là hệ thống quan sát và điều chỉnh năng lượng môi trường xung quanh để mang lại may mắn, thịnh vượng. Phong Thủy liên quan mật thiết với Bazi vì mỗi người có năng lượng riêng và cần môi trường phù hợp để phát triển. Các yếu tố Phong Thủy bao gồm: hướng nhà, vị trí, bố trí nội thất, màu sắc, vật liệu.

Khi kết hợp Bazi và Phong Thủy, hệ thống có thể đưa ra đề xuất cá nhân hóa cao. Ví dụ người thiên về Mộc cần hướng Đông, màu xanh lá, nội thất bằng gỗ. Tính năng này có thể tích hợp vào ứng dụng dưới dạng quiz hoặc kết hợp với thông tin Bazi để tự động đề xuất. Đây là hướng phát triển giá trị gia tăng cho sản phẩm.

### 17. Hóa (化 - Transformation/Transmutation)

Hóa là quá trình biến đổi năng lượng của một yếu tố thành yếu tố khác dưới ảnh hưởng của các yếu tố xung quanh. Trong Bazi, có ba loại Hóa chính: Hóa Can (biến đổi thiên can), Hóa Chi (biến đổi địa chi), Hóa Khí (biến đổi năng lượng tổng thể). Hóa xảy ra khi các yếu tố trong lá số có mối quan hệ tương tác đủ mạnh để tạo ra sự biến đổi.

Hóa là khái niệm phức tạp nhưng quan trọng trong việc phân tích sâu lá số. Ví dụ một người có Mộc quá mạnh có thể được Hóa thành Hỏa nếu trong lá số có nhiều Hỏa. Điều này có nghĩa là năng lượng dư thừa không bị lãng phí mà được chuyển hóa thành năng lượng khác. Trong AI, Hóa cần được mô hình hóa dưới dạng các quy tắc hoặc neural network layers.

### 18. Quái Số (卦數 - Trigram Numbers)

Quái Số là các con số từ 1 đến 9 được gán cho mỗi cung trong bát quái, dùng để tính toán các chỉ số phong thủy. Mỗi quái số tương ứng với một ngũ hành và có ý nghĩa riêng. Quái Số được sử dụng trong nhiều ứng dụng Bazi: tính số nhà, số xe, ngày giờ hợp lý, và phân tích các mối quan hệ.

Trong lập trình, Quái Số được lưu trữ như một enum hoặc constant object với các thuộc tính: số, tên quái, ngũ hành, hướng, màu sắc. Khi người dùng nhập số nhà hoặc số xe, hệ thống tự động tính Quái Số và đánh giá mức độ phù hợp với lá số của họ. Đây là tính năng thường được người dùng quan tâm và có tỷ lệ sử dụng cao.

## Kết luận

Từ điển thuật ngữ này là nền tảng để xây dựng hệ thống Bazi chính xác và chuyên nghiệp. Tất cả các thuật ngữ cần được implement đúng ý nghĩa và mối quan hệ của chúng trong codebase. Việc hiểu rõ từng thuật ngữ giúp developer tạo ra sản phẩm có giá trị thực sự cho người dùng.
